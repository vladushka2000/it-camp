"""insert_history_action_types

Revision ID: cebf469e5bf8
Revises: 89fcb53dc9c4
Create Date: 2024-08-22 23:33:47.015971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cebf469e5bf8'
down_revision: Union[str, None] = '89fcb53dc9c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO
            history_action_type (id, name)
        VALUES
            ('7fefea33-46f6-4b63-986b-4184742efd6a', 'Загрузка магнитограммы'),
            ('5b329d90-98aa-49ed-b01a-f7d85c0b17c6', 'Редактирование магнитограммы');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM
            history_action_type
        WHERE id IN (
            '7fefea33-46f6-4b63-986b-4184742efd6a',
            '5b329d90-98aa-49ed-b01a-f7d85c0b17c6'
        );
        """
    )
