import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model
from repositories.models import user_model  # no qa


class Role(base_alchemy_model.Base):
    """
    Модель Алхимии для роли пользователя
    """

    __tablename__ = "role"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор пользователя",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Название роли")
