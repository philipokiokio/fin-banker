# 3rd party imports
from sqlalchemy import Column, ForeignKey, DECIMAL, String, Integer, UUID
import uuid
from sqlalchemy.orm import relationship

# application imports
from src.app.utils.models_utils import AbstractModel


class Account(AbstractModel):
    __tablename__ = "accounts"
    balance = Column(DECIMAL(scale=2))
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", passive_deletes=True)


class Transaction(AbstractModel):
    __tablename__ = "transactions"
    tranzact_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    amount = Column(DECIMAL(scale=2))
    status = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reciever_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    sender = relationship(
        "User",
        primaryjoin="Transaction.sender_id == User.id",
    )
    reciever = relationship(
        "User",
        primaryjoin="Transaction.reciever_id == User.id",
    )
