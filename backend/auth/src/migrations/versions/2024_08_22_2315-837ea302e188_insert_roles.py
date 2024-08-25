"""insert_roles

Revision ID: 837ea302e188
Revises: 8ae4ef6c3c84
Create Date: 2024-08-22 23:15:25.935112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '837ea302e188'
down_revision: Union[str, None] = '8ae4ef6c3c84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO
            role (id, name)
        VALUES
            ('f1ffeaba-e4ca-4c6b-91fc-2fcd004fb7ec', 'Expert');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM role WHERE id = 'f1ffeaba-e4ca-4c6b-91fc-2fcd004fb7ec';
        """
    )
