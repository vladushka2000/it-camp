import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from interfaces import base_alchemy_model
from repositories.models import magnetogram_model  # no qa


class Report(base_alchemy_model.Base):
    """
    Модель Алхимии для отчета
    """

    __tablename__ = "report"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор отчета",
        default=lambda: str(uuid.uuid4()),
    )
    magnetogram_id = sa.Column(sa.UUID, sa.ForeignKey("magnetogram.id"), comment="Идентификатор магнитограммы")
    magnetogram = orm.relationship("Magnetogram", back_populates="reports", lazy="joined")
    report = sa.Column(sa.LargeBinary, comment="Отчет в формате PDF", nullable=False)
    user_name = sa.Column(sa.String, comment="Имя пользователя", nullable=False)
    created_at = sa.Column(
        sa.DateTime, comment="Дата создания", default=datetime.datetime.now(), nullable=False
    )
