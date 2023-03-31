from fastapi import Depends, status, HTTPException
from src.auth.models import User
from src.auth.oauth import get_current_user
from src.accounts.schemas import TranzactionCreate
from src.accounts.account_repo import account_repo, Account
from decimal import Decimal
from uuid import UUID
from src.accounts.account_repo import transaction_repo


# Admin PIPES
def admin_user_dep(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            detail="user does not have the permission to carry out such action",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return current_user


# CHECK IF SENDER HAS SUFFICIENT BALANCE
def can_send_dep(
    amount: str,
    current_user: User = Depends(get_current_user),
):
    user_balance: Account = account_repo.get_balance(current_user.id)
    if user_balance.balance < Decimal(amount):
        raise HTTPException(
            detail="sender has insufficient balance to complete this transaction",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return current_user


# CHECKS THAT ACTION IS CARRIED OUT BY RECIEVER AND LOCKS ACTION TO ONCE
def is_reciever_dep(
    tranzact_id: UUID,
    current_user: dict = Depends(get_current_user),
):
    tranzaction = transaction_repo.get_by_tranzact_id(tranzact_id)

    if not tranzaction:
        raise HTTPException(
            detail="Tranzaction does not exist", status_code=status.HTTP_404_NOT_FOUND
        )

    if tranzaction.status != "Sent":
        raise HTTPException(
            detail="Tranzaction resolved", status_code=status.HTTP_409_CONFLICT
        )
    else:
        if tranzaction.reciever_id != current_user.id:
            raise HTTPException(
                detail="User is not the recipient of this tranzaction",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    return current_user


# LOCK REVERT ACTION TO ONE FOR ADMINS.
def is_reverted_dep(tranzact_id: UUID, current_user: dict = Depends(admin_user_dep)):
    tranzaction = transaction_repo.get_by_tranzact_id(tranzact_id)

    if not tranzaction:
        raise HTTPException(
            detail="Tranzaction does not exist", status_code=status.HTTP_404_NOT_FOUND
        )

    if tranzaction.status == "Reverted" or tranzaction.status == "Rejected":
        raise HTTPException(
            detail="Tranzaction block is closed", status_code=status.HTTP_409_CONFLICT
        )

    return current_user
