import datetime
import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class Magnetogram(base_alchemy_model.Base):
    """
    Модель Алхимии для магнитограмм
    """

    __tablename__ = "magnetogram"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор магнитограммы",
        default=lambda: str(uuid.uuid4()),
    )
    object_name = sa.Column(sa.String, comment="Название объекта", nullable=False)
    user_name = sa.Column(sa.String, comment="Имя пользователя", nullable=False)
    comment = sa.Column(sa.String, comment="Комментарий")
    magnetogram = sa.Column(sa.LargeBinary, comment="Магнитограмма в формате png", nullable=False)
    created_at = sa.Column(
        sa.DateTime, comment="Дата создания", default=datetime.datetime.now(), nullable=False
    )
