"""Accounts for user

Revision ID: 39a139c2fbb9
Revises: b59eb2cd4e8c
Create Date: 2023-03-30 15:16:44.724461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "39a139c2fbb9"
down_revision = "b59eb2cd4e8c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer),
        sa.Column("balance", sa.DECIMAL(scale=2)),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_table("accounts")
    pass
