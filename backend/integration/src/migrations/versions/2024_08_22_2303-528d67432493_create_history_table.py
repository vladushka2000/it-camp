"""create_history_table

Revision ID: 528d67432493
Revises: fa1c18256c83
Create Date: 2024-08-22 23:03:47.057451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '528d67432493'
down_revision: Union[str, None] = 'fa1c18256c83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор отчета'),
    sa.Column('magnetogram_id', sa.UUID(), nullable=False, comment='Идентификатор магнитограммы'),
    sa.Column('action_type_id', sa.UUID(), nullable=False, comment='Идентификатор действия пользователя'),
    sa.Column('date', sa.DateTime(), nullable=False, comment='Дата записи'),
    sa.Column('user_name', sa.String(), nullable=False, comment='Имя пользователя'),
    sa.ForeignKeyConstraint(['action_type_id'], ['history_action_type.id'], ),
    sa.ForeignKeyConstraint(['magnetogram_id'], ['magnetogram.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    # ### end Alembic commands ###
