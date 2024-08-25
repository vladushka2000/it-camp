import uuid

import sqlalchemy as sa

from interfaces import base_alchemy_model


class StructuralUnit(base_alchemy_model.Base):
    """
    Модель Алхимии для структурных элементов
    """

    __tablename__ = "structural_unit"

    id = sa.Column(
        sa.UUID,
        primary_key=True,
        comment="Идентификатор структурного элемента",
        default=lambda: str(uuid.uuid4()),
    )
    type_id = sa.ForeignKey(
        "structural_unit_type.id",
        comment="Идентификатор типа структурного элемента",
        nullable=False
    )
    continue_for = sa.Column(
        sa.Integer,
        comment="Количество таких же структурных элементов справа по оси X",
        default=0,
        nullable=False
    )
    x_coord = sa.Column(sa.Integer, comment="Координата по оси X", nullable=False)
