import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class MagnetogramStructuralUnit(base_alchemy_model.Base):
    """
    Модель Алхимии для связи many-to-many таблиц magnetogram и structural_unit
    """

    __tablename__ = "magnetogram_structural_unit"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор связи",
        default=lambda: str(uuid.uuid4()),
    )
    magnetogram_id = sa.ForeignKey("magnetogram.id", comment="Идентификатор магнитограммы", nullable=False)
    structural_unit_id = sa.ForeignKey(
        "structural_unit.id",
        comment="Идентификатор структурного элемента",
        nullable=False
    )
