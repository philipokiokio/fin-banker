"""transfer tables

Revision ID: 0d067824e076
Revises: 39a139c2fbb9
Create Date: 2023-03-30 18:39:11.322135

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = "0d067824e076"
down_revision = "39a139c2fbb9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer),
        sa.Column(
            "tranzact_id", sa.UUID(as_uuid=True), default=uuid.uuid4, unique=True
        ),
        sa.Column("amount", sa.DECIMAL(scale=2)),
        sa.Column("sender_id", sa.Integer, nullable=False),
        sa.Column("reciever_id", sa.Integer, nullable=False),
        sa.Column("status", sa.String),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reciever_id"], ["users.id"], ondelete="CASCADE"),
    )

    pass


def downgrade() -> None:
    op.drop_table("transactions")
    pass
