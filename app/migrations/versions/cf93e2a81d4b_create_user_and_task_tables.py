"""Create User and Task tables

Revision ID: cf93e2a81d4b
Revises: 2d5ccd2f24c2
Create Date: 2024-10-30 22:42:48.260465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf93e2a81d4b'
down_revision: Union[str, None] = '2d5ccd2f24c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
