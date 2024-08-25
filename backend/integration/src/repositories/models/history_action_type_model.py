import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class HistoryActionType(base_alchemy_model.Base):
    """
    Модель Алхимии для типов действий пользователя в системе
    """

    __tablename__ = "history_action_type"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор типа действия",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Название типа действия", nullable=False)
