from typing import List, Union
from src.accounts.account_repo import (
    transaction_repo,
    Transaction,
    account_repo,
    Account,
)
from src.accounts import schemas
from src.auth.models import User
from uuid import uuid4
from decimal import Decimal
from fastapi import HTTPException, status
from src.auth.auth_repository import user_repo


# SERVICE FOR TRANSACTIONS CRUD AND ADMIN ACTIONS
class TranzactService:
    def __init__(self) -> None:
        self.repo = transaction_repo
        self.account = account_repo
        self.user = user_repo

    def race_check(self, account: Account, amount: Decimal):
        if account.balance < amount:
            raise HTTPException(
                detail="Sender has insufficient Balance for this transaction",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def tranzact_check(self, tranzact: Union[List[Transaction], Transaction]):
        if not tranzact:
            raise HTTPException(
                detail="tranzaction does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def orm_call(self, tranzact: Transaction):
        tranzact_ = tranzact.__dict__
        tranzact_["reciever"] = tranzact.reciever
        tranzact_["sender"] = tranzact.sender
        return tranzact_

    def create(self, tranzact_create: schemas.TranzactionCreate, current_user: User):
        sender_account = self.account.get_balance(current_user.id)
        user_check = self.user.get_by_username(tranzact_create.reciever_username)
        if not user_check:
            raise HTTPException(
                detail="user not found", status_code=status.HTTP_404_NOT_FOUND
            )

        tranzact_dict = tranzact_create.dict()
        del tranzact_dict["reciever_username"]

        tranzact_dict["tranzact_id"] = uuid4()
        tranzact_dict["amount"] = Decimal(tranzact_create.amount)
        tranzact_dict["status"] = schemas.StatusOptions.sent.value
        tranzact_dict["sender_id"] = current_user.id
        tranzact_dict["reciever_id"] = user_check.id

        self.race_check(sender_account, Decimal(tranzact_dict["amount"]))

        tranzact = self.repo.create(tranzact_dict)

        sender_account.balance = sender_account.balance - tranzact.amount
        self.account.update(sender_account)

        tranzact = self.orm_call(tranzact)

        return {
            "message": "transaction is sent successfully",
            "data": tranzact,
            "status": status.HTTP_201_CREATED,
        }

    def update(
        self,
        tranzaction_id: str,
        tranzact_update: schemas.TranzactUpdate,
        current_user: User,
    ):
        tranzaction = self.repo.get_by_tranzact_id(tranzaction_id)
        self.tranzact_check(tranzaction)

        if tranzact_update.is_accepted is False:
            tranzaction.status = schemas.StatusOptions.rejected.value
            sender_account = self.account.get_balance(tranzaction.sender_id)
            sender_account.balance = sender_account.balance + tranzaction.amount
            self.account.update(sender_account)

        else:
            tranzaction.status = schemas.StatusOptions.accepted.value

            reciever_account = self.account.get_balance(tranzaction.reciever_id)
            reciever_account.balance = reciever_account.balance + tranzaction.amount
            self.account.update(reciever_account)

        self.repo.update(tranzaction)

        tranzact = self.orm_call(tranzaction)

        return {
            "message": "tranzaction updated successfully",
            "data": tranzact,
            "status": status.HTTP_200_OK,
        }

    def revert_update(self, tranzaction_id: str, current_user: User):
        tranzaction = self.repo.get_by_tranzact_id(tranzaction_id)

        self.tranzact_check(tranzaction)

        if tranzaction.status == schemas.StatusOptions.sent.value:
            sender_account = self.account.get_balance(tranzaction.sender_id)
            sender_account.balance = tranzaction.amount + sender_account.balance
            self.account.update(sender_account)

        elif tranzaction.status == schemas.StatusOptions.accepted.value:
            reciever_account = self.account.get_balance(tranzaction.reciever_id)
            reciever_account.balance = reciever_account.balance - tranzaction.amount
            self.account.update(reciever_account)

            # Sender update
            sender_account = self.account.get_balance(current_user.id)
            sender_account.balance = tranzaction.amount + sender_account.balance
            self.account.update(sender_account)

        tranzaction.status = schemas.StatusOptions.reverted.value
        self.repo.update(tranzaction)

        tranzact = self.orm_call(tranzaction)

        return {
            "message": "tranzaction reverted successfully",
            "data": tranzact,
            "status": status.HTTP_200_OK,
        }

    def get_tranzactions(self):
        tranzactions = self.repo.get()
        self.tranzact_check(tranzactions)

        tranzactions_ = []

        for tranzact in tranzactions:
            tranzactions_.append(self.orm_call(tranzact))

        return {
            "message": "tranzactions returned sucessfully",
            "data": tranzactions_,
            "status": status.HTTP_200_OK,
        }

    def get_user_tranzactions(self, current_user: User):
        tranzactions = self.repo.get_user_tranzact(current_user.id)
        self.tranzact_check(tranzactions)

        tranzactions_ = []

        for tranzact in tranzactions:
            tranzactions_.append(self.orm_call(tranzact))

        return {
            "message": "tranzactions returned sucessfully",
            "data": tranzactions_,
            "status": status.HTTP_200_OK,
        }

    def get_tranzaction(self, tranzact_id: str):
        tranzaction = self.repo.get_by_tranzact_id(tranzact_id)
        self.tranzact_check(tranzaction)
        tranzaction_ = self.orm_call(tranzaction)
        return {
            "message": "tranzaction retrieved successfully",
            "data": tranzaction_,
            "status": status.HTTP_200_OK,
        }


tranzact_service = TranzactService()
