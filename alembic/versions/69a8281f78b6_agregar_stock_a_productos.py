"""agregar stock a productos

Revision ID: 69a8281f78b6
Revises: f5fdec8432b0
Create Date: 2026-08-31 08:48:06.784773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69a8281f78b6"
down_revision: Union[str, Sequence[str], None] = "f5fdec8432b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "productos",
        sa.Column("stock", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("productos", "stock")