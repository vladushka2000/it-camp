import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class MagnetogramDefect(base_alchemy_model.Base):
    """
    Модель Алхимии для связи many-to-many таблиц magnetogram и defect
    """

    __tablename__ = "magnetogram_defect"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор связи",
        default=lambda: str(uuid.uuid4()),
    )
    magnetogram_id = sa.ForeignKey("magnetogram.id", comment="Идентификатор магнитограммы", nullable=False)
    defect_id = sa.ForeignKey("defect.id", comment="Идентификатор дефекта", nullable=False)
