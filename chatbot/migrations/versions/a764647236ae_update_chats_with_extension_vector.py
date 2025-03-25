"""update chats with extension vector

Revision ID: a764647236ae
Revises: a75897f96a09
Create Date: 2025-02-24 16:42:25.074619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a764647236ae'
down_revision: Union[str, None] = 'a75897f96a09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'chats', ['id'])
    op.create_unique_constraint(None, 'contents', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contents', type_='unique')
    op.drop_constraint(None, 'chats', type_='unique')
    # ### end Alembic commands ###
