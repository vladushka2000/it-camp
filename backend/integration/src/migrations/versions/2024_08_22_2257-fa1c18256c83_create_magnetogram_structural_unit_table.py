"""create_magnetogram_structural_unit_table

Revision ID: fa1c18256c83
Revises: 4218af1645d4
Create Date: 2024-08-22 22:57:49.833495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa1c18256c83'
down_revision: Union[str, None] = '4218af1645d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('magnetogram_structural_unit',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор связи'),
    sa.Column('magnetogram_id', sa.UUID(), nullable=True, comment='Идентификатор магнитограммы'),
    sa.Column('structural_unit_id', sa.UUID(), nullable=True, comment='Идентификатор структурного элемента'),
    sa.ForeignKeyConstraint(['magnetogram_id'], ['magnetogram.id'], ),
    sa.ForeignKeyConstraint(['structural_unit_id'], ['structural_unit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('magnetogram_structural_unit')
    # ### end Alembic commands ###
