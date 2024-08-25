import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class Defect(base_alchemy_model.Base):
    """
    Модель Алхимии для дефектов
    """

    __tablename__ = "defect"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор дефекта",
        default=lambda: str(uuid.uuid4()),
    )
    type_id = sa.ForeignKey("defect_type.id", comment="Идентификатор типа дефекта", nullable=False)
    continue_for = sa.Column(
        sa.Integer,
        comment="Количество таких же дефектов справа по оси X",
        default=0,
        nullable=False
    )
    x_coord = sa.Column(sa.Integer, comment="Координата по оси X", nullable=False)
