from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.pipes.account_deps import (
    admin_user_dep,
    can_send_dep,
    is_reciever_dep,
    is_reverted_dep,
)
from src.accounts import schemas
from src.accounts.account_service import tranzact_service
from src.auth.oauth import get_current_user

# ACCOUNT ROUTER
account_router = APIRouter(prefix="/api/v1/transaction", tags=["Tranzactions"])


@account_router.post(
    "/transfer/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageTranzactResp,
)
def transfer_fund(
    amount: str,
    tranzact_create: schemas.TranzactionCreate,
    current_user: dict = Depends(can_send_dep),
):
    return tranzact_service.create(tranzact_create, current_user)


@account_router.get(
    "s/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListTranzactResp,
)
def user_tranzactions(
    current_user: dict = Depends(get_current_user),
):
    return tranzact_service.get_user_tranzactions(current_user)


@account_router.get(
    "/{tranzact_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageTranzactResp,
)
def get_tranzaction(
    tranzact_id: UUID,
    current_user: dict = Depends(get_current_user),
):
    return tranzact_service.get_tranzaction(tranzact_id)


@account_router.patch(
    "/{tranzact_id}/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageTranzactResp,
)
def update_tranzaction(
    tranzact_id: UUID,
    tranzact_update: schemas.TranzactUpdate,
    current_user: dict = Depends(is_reciever_dep),
):
    return tranzact_service.update(tranzact_id, tranzact_update, current_user)


@account_router.get(
    "s/admin/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListTranzactResp,
)
def user_tranzactions(
    current_user: dict = Depends(admin_user_dep),
):
    return tranzact_service.get_tranzactions()


@account_router.patch(
    "/{tranzact_id}/revert/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageTranzactResp,
)
def revert_tranzaction(
    tranzact_id: UUID,
    current_user: dict = Depends(is_reverted_dep),
):
    return tranzact_service.revert_update(tranzact_id, current_user)
