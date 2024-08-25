"""create_history_action_type_table

Revision ID: 88593a2c2db9
Revises: 5183d8003581
Create Date: 2024-08-22 22:56:32.237466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88593a2c2db9'
down_revision: Union[str, None] = '5183d8003581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history_action_type',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор типа действия'),
    sa.Column('name', sa.String(), nullable=False, comment='Название типа действия'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history_action_type')
    # ### end Alembic commands ###
