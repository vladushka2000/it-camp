import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from interfaces import base_alchemy_model
from repositories.models import magnetogram_model  # no qa


class DefectType(base_alchemy_model.Base):
    """
    Модель Алхимии для типов дефектов
    """

    __tablename__ = "defect_type"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор типа дефекта",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Название типа дефекта", nullable=False)
    defects = orm.relationship("Defect", back_populates="type")
