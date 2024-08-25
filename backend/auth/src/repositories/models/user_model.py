import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from interfaces import base_alchemy_model
from repositories.models import role_model  # no qa


class User(base_alchemy_model.Base):
    """
    Модель Алхимии для пользователя
    """

    __tablename__ = "user"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор пользователя",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Хешированный пароль")
    role_id = sa.Column(
        sa.UUID, sa.ForeignKey("role.id"), comment="Идентификатор роли пользователя"
    )
    role = orm.relationship("Role", backref="user")
    created_at = sa.Column(
        sa.DateTime, comment="Дата регистрации", default=datetime.datetime.now()
    )
