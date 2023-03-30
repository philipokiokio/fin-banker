# 3rd party imports
from sqlalchemy import Boolean, Column, ForeignKey, String, text, DECIMAL
from sqlalchemy.orm import relationship

# application imports
from src.app.utils.models_utils import AbstractModel


class User(AbstractModel):
    # User Table
    __tablename__ = "users"
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))
    account = relationship("Account", back_populates="user", passive_deletes=True)
    debit_logs = relationship(
        "Transaction",
        back_populates="sender",
        foreign_keys="Transaction.sender_id",
        passive_deletes=True,
    )
    credit_logs = relationship(
        "Transaction",
        back_populates="reciever",
        foreign_keys="Transaction.reciever_id",
        passive_deletes=True,
    )


class RefreshToken(AbstractModel):
    # Refresh Token Table
    __tablename__ = "user_refresh_token"
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    user = relationship("User", passive_deletes=True)
