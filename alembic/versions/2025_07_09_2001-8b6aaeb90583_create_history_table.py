"""create history table

Revision ID: 8b6aaeb90583
Revises: 3d90e3ca13e5
Create Date: 2025-07-09 20:01:22.174543

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b6aaeb90583"
down_revision: Union[str, Sequence[str], None] = "3d90e3ca13e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "histories",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("histories")
    # ### end Alembic commands ###
