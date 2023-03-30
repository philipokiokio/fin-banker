# framework imports
from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# application imports
from src.auth import schemas
from src.auth.auth_service import user_service
from src.auth.oauth import get_current_user, verify_refresh_token
from src.pipes.account_deps import admin_user_dep

# API Router
user_router = APIRouter(prefix="/api/v1/auth", tags=["User Authentication"])


@user_router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageUserResponse,
)
async def register(user_create: schemas.user_create):
    """Registration of User

    Args:
        user_create (schemas.user_create): {
        "first_name", "last_name","email", "password"
        }

    Returns:
        _type_: response
    """
    new_user = await user_service.register(user_create)
    return {
        "message": "Registration Successful",
        "data": new_user,
        "status": status.HTTP_201_CREATED,
    }


@user_router.post(
    "/register/admin/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageUserResponse,
)
async def register_admin(user_create: schemas.user_create):
    """Registration of User

    Args:
        user_create (schemas.user_create): {
        "first_name", "last_name","email", "password"
        }

    Returns:
        _type_: response
    """
    new_user = await user_service.register_admin(user_create)
    return {
        "message": "Registration Successful",
        "data": new_user,
        "status": status.HTTP_201_CREATED,
    }


@user_router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageLoginResponse,
)
def login(login_user: OAuth2PasswordRequestForm = Depends()):
    """Login

    Args:
        login_user (OAuth2PasswordRequestForm, optional):username, password

    Returns:
        _type_: user
    """
    user_login = user_service.login(login_user)
    return user_login


@user_router.get(
    "/me/", status_code=status.HTTP_200_OK, response_model=schemas.MessageUserResponse
)
def logged_in_user(current_user: dict = Depends(get_current_user)):
    """ME

    Args:
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): User data.

    Returns:
        _type_: User
    """
    return {"message": "Me Data", "data": current_user, "status": status.HTTP_200_OK}


@user_router.patch(
    "/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageUserResponse,
)
def update_user(
    update_user: schemas.UserUpdate, current_user: dict = Depends(get_current_user)
):
    """Update User

    Args:
        update_user (schemas.UserUpdate): all user fields.
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User.

    Returns:
        _type_: resp
    """
    update_user = user_service.update_user(update_user, current_user)

    return {
        "message": "User Updated Successfully",
        "data": update_user,
        "status": status.HTTP_200_OK,
    }


@user_router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: dict = Depends(get_current_user)):
    """Delete User

    Args:
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User

    Returns:
        _type_: 204
    """
    user_service.delete(current_user)
    return {"status": status.HTTP_204_NO_CONTENT}


@user_router.get("/refresh/", status_code=status.HTTP_200_OK)
def get_new_token(new_access_token: str = Depends(verify_refresh_token)):
    """New Access token

    Args:
        new_access_token (str, optional): _description_. Defaults to Depends(verify_refresh_token): Gets Access token based on refresh token.

    Returns:
        _type_: _description_
    """
    return {
        "message": "New access token created successfully",
        "token": new_access_token,
        "status": status.HTTP_200_OK,
    }


@user_router.patch(
    "/change-password/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageUserResponse,
)
def change_password(
    password_data: schemas.ChangePassword,
    current_user: dict = Depends(get_current_user),
):
    """Change Password

    Args:
        password_data (schemas.ChangePassword): {password, old_password}
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User

    Returns:
        _type_: response
    """
    resp = user_service.change_password(current_user, password_data)
    return resp


@user_router.get(
    "/all-users/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListUserResponse,
)
def admin_users(current_user: dict = Depends(admin_user_dep)):
    resp = user_service.get_users
    return resp
