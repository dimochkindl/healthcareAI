"""init1234

Revision ID: a75897f96a09
Revises: 
Create Date: 2025-02-24 16:14:22.612044

"""
from typing import Sequence, Union

import pgvector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a75897f96a09'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_query_id', sa.String(), nullable=True),
    sa.Column('prompt', sa.ARRAY(sa.JSON()), server_default='{}', nullable=True),
    sa.Column('user_query', sa.String(), nullable=True),
    sa.Column('assistant_answer', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('contents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contents')
    op.drop_table('chats')
    # ### end Alembic commands ###
