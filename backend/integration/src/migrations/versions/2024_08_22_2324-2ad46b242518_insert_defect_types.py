"""insert_defect_types

Revision ID: 2ad46b242518
Revises: 528d67432493
Create Date: 2024-08-22 23:24:03.399428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ad46b242518'
down_revision: Union[str, None] = '528d67432493'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO
            defect_type (id, name)
        VALUES
            ('985c9151-5446-4130-ae65-755baef7ac63', 'Отсутствие'),
            ('e817ad05-c8b6-4f26-be95-ce9bf20b7822', 'Присутствие');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM
            defect_type
        WHERE id IN (
            '985c9151-5446-4130-ae65-755baef7ac63',
            'e817ad05-c8b6-4f26-be95-ce9bf20b7822'
        );
        """
    )

