from src.app.utils.schemas_utils import (
    AbstractModel,
    ResponseModel,
    StatusOptions,
    User,
)
from decimal import Decimal
from typing import List


class TranzactionCreate(AbstractModel):
    amount: str
    reciever_username: str


class TransactResp(AbstractModel):
    tranzact_id: str
    amount: Decimal
    sender: User
    reciever: User
    status: str


class MessageTranzactResp(ResponseModel):
    data: TransactResp


class MessageListTranzactResp(ResponseModel):
    data: List[TransactResp]


class TranzactUpdate(AbstractModel):
    is_accepted: bool
