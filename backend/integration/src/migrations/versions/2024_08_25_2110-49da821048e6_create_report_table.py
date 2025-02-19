"""create_report_table

Revision ID: 49da821048e6
Revises: cebf469e5bf8
Create Date: 2024-08-25 21:10:54.983449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49da821048e6'
down_revision: Union[str, None] = 'cebf469e5bf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор отчета'),
    sa.Column('magnetogram_id', sa.UUID(), nullable=False, comment='Идентификатор магнитограммы'),
    sa.Column('report', sa.LargeBinary(), nullable=False, comment='Отчет в формате PDF'),
    sa.Column('user_name', sa.String(), nullable=False, comment='Имя пользователя'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='Дата создания'),
    sa.ForeignKeyConstraint(['magnetogram_id'], ['magnetogram.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report')
    # ### end Alembic commands ###
