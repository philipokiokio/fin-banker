from fastapi import Depends, status, HTTPException
from src.auth.models import User
from src.auth.oauth import get_current_user
from src.accounts.schemas import TranzactionCreate
from src.accounts.account_repo import account_repo, Account


def admin_user_dep(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            detail="user does not have the permission to carry out such action",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return current_user


def can_sender_dep(
    tranzact_create: TranzactionCreate = Depends(),
    current_user: User = Depends(get_current_user),
):
    user_balance: Account = account_repo.get_balance(current_user.id)

    if user_balance.balance < tranzact_create.amount:
        raise HTTPException(
            detail="sender has insufficient balance to complete this transaction",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return current_user
