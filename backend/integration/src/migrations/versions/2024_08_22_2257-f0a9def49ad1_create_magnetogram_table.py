"""create_magnetogram_table

Revision ID: f0a9def49ad1
Revises: 8ed740b6416c
Create Date: 2024-08-22 22:57:24.086429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a9def49ad1'
down_revision: Union[str, None] = '8ed740b6416c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('magnetogram',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор магнитограммы'),
    sa.Column('object_name', sa.String(), nullable=False, comment='Название объекта'),
    sa.Column('user_name', sa.String(), nullable=False, comment='Имя пользователя'),
    sa.Column('comment', sa.String(), nullable=True, comment='Комментарий'),
    sa.Column('magnetogram', sa.LargeBinary(), nullable=False, comment='Магнитограмма в формате png'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='Дата создания'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('magnetogram')
    # ### end Alembic commands ###
