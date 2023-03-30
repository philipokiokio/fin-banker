# Framework Imports
from decimal import Decimal
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# application imports
from src.app.utils.db_utils import hash_password, verify_password
from src.app.utils.token import auth_settings, auth_token
from src.auth import schemas
from src.auth.auth_repository import token_repo, user_repo
from src.auth.models import RefreshToken, User
from src.auth.oauth import (
    create_access_token,
    create_refresh_token,
    credential_exception,
)
from src.accounts.account_repo import account_repo


class UserService:
    def __init__(self):
        # Initializing Repositories
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.account_repo = account_repo

    def orm_call(self, user: User):
        user_ = user.__dict__
        if user.account:
            user_["account"] = user.account
        if user.debit_logs:
            user_["debits"] = user.debit_logs
        if user.credit_logs:
            user_["credits"] = user.credit_logs
        return user_

    async def register(self, user: schemas.user_create) -> User:
        # checking if user exists.
        user_check = self.user_repo.get_user(user.email)

        # raise an Exception if user exists.
        if user_check:
            raise HTTPException(
                detail="This User has an account",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # password hashing
        user.password = hash_password(user.password)
        # creating new user
        user_ = user.dict()
        new_user = self.user_repo.create(user_)
        account_dict = {"user_id": new_user.id, "balance": Decimal("1000.00")}
        self.account_repo.create(account_dict)

        return self.orm_call(new_user)

    async def register_admin(self, user: schemas.user_create) -> User:
        # checking if user exists.
        user_check = self.user_repo.get_user(user.email)

        # raise an Exception if user exists.
        if user_check:
            raise HTTPException(
                detail="This User has an account",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # password hashing
        user.password = hash_password(user.password)
        user_ = user.dict()
        user_["is_admin"] = True
        # creating new user
        new_user = self.user_repo.create(user_)
        return self.orm_call(new_user)

    def login(self, user: OAuth2PasswordRequestForm) -> schemas.LoginResponse:
        # check if user exists.
        user_check = self.user_repo.get_user(user.username)
        # raise exception if there is no user
        if not user_check:
            raise HTTPException(
                detail="User does not exist", status_code=status.HTTP_400_BAD_REQUEST
            )
        # verify that the password is correct.
        pass_hash_check = verify_password(user_check.password, user.password)
        # raise credential error
        if not pass_hash_check:
            credential_exception()

        # create Access and Refresh Token
        token_data = {"email": user_check.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        # check if there is a previously existing refresh token
        token_check = self.token_repo.get_token(user_check.id)
        # if token update token column
        if token_check:
            token_check.token = refresh_token
            self.token_repo.update_token(token_check)
        else:
            # create new token data
            self.token_repo.create_token(refresh_token, user_check.id)

        # validating data via the DTO
        refresh_token_ = {"token": refresh_token, "header": "Refresh-Tok"}
        login_resp = schemas.LoginResponse(
            data=self.orm_call(user_check),
            refresh_token=refresh_token_,
        )
        # DTO response
        resp = {
            "message": "Login Successful",
            "data": login_resp,
            "access_token": access_token,
            "token_type": "bearer",
            "status": status.HTTP_200_OK,
        }
        return resp

    def update_user(self, update_user: schemas.UserUpdate, user: User) -> User:
        # update user
        update_user_dict = update_user.dict(exclude_unset=True)

        for key, value in update_user_dict.items():
            setattr(user, key, value)

        return self.orm_call(self.user_repo.update(user))

    def delete(self, user: User) -> bool:
        # delete user
        return self.user_repo.delete(user)

    def change_password(self, user: User, password_data: schemas.ChangePassword):
        # verify oldpassword is saved in the DB
        password_check = verify_password(user.password, password_data.old_password)
        # if not True raise Exception
        if not password_check:
            raise HTTPException(
                detail="Old Password does not corelate.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # hash new password
        user.password = hash_password(password_data.password)
        # update user
        user = self.user_repo.update(user)
        # return user
        return {
            "message": "Password changed successfully",
            "data": self.orm_call(user),
            "status": status.HTTP_200_OK,
        }

    @property
    def get_users(self):
        users = self.user_repo.get_users
        if not users:
            raise HTTPException(
                detail="no user on finbanker", status_code=status.HTTP_404_NOT_FOUND
            )
        users_ = []

        for user in users:
            users_.append(self.orm_call(user))

        return {
            "message": "all users on fin-banker retrieved successfully",
            "data": users_,
            "status": status.HTTP_200_OK,
        }


# Instanting the UserService class
user_service = UserService()
