import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from interfaces import base_alchemy_model
from repositories.models import magnetogram_model  # no qa


class StructuralUnitType(base_alchemy_model.Base):
    """
    Модель Алхимии для типов структурных элементов
    """

    __tablename__ = "structural_unit_type"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор типа структорного элемента",
        default=lambda: str(uuid.uuid4()),
    )
    name = sa.Column(sa.String, comment="Название типа структурного элемента", nullable=False)
    structural_units = orm.relationship("StructuralUnit", back_populates="type")
