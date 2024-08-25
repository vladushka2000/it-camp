import datetime
import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class History(base_alchemy_model.Base):
    """
    Модель Алхимии для истории загрузок
    """

    __tablename__ = "history"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор отчета",
        default=lambda: str(uuid.uuid4()),
    )
    magnetogram_id = sa.Column(
        sa.UUID, sa.ForeignKey("magnetogram.id"), comment="Идентификатор магнитограммы", nullable=False
    )
    action_type_id = sa.Column(
        sa.UUID, sa.ForeignKey("history_action_type.id"), comment="Идентификатор действия пользователя", nullable=False
    )
    date = sa.Column(
        sa.DateTime, comment="Дата записи", default=datetime.datetime.now(), nullable=False
    )
    user_name = sa.Column(sa.String, comment="Имя пользователя", nullable=False)
