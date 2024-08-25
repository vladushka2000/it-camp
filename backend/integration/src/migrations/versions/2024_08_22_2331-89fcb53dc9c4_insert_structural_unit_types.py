"""insert_structural_unit_types

Revision ID: 89fcb53dc9c4
Revises: 2ad46b242518
Create Date: 2024-08-22 23:31:46.043683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89fcb53dc9c4'
down_revision: Union[str, None] = '2ad46b242518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO
            structural_unit_type (id, name)
        VALUES
            ('7d2a4cf4-0c2e-446b-bfc3-c11aed172725', 'Отсутствие'),
            ('3e058c22-8452-4a0a-b0fa-368f5e205912', 'Сварной шов'),
            ('94950972-c06f-4bc0-92b7-76c23b8a5295', 'Изгиб'),
            ('a16b87aa-b6ed-4910-8412-8adb37ad943d', 'Разветвление'),
            ('dc3690d8-b52d-4cd3-829a-2e2223813e40', 'Заплатка');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM
            structural_unit_type
        WHERE id IN (
            '7d2a4cf4-0c2e-446b-bfc3-c11aed172725',
            '3e058c22-8452-4a0a-b0fa-368f5e205912',
            '94950972-c06f-4bc0-92b7-76c23b8a5295',
            'a16b87aa-b6ed-4910-8412-8adb37ad943d',
            'dc3690d8-b52d-4cd3-829a-2e2223813e40'
        );
        """
    )
