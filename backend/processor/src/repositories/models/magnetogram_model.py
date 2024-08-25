from __future__ import annotations  # no qa

import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from interfaces import base_alchemy_model
from repositories.models import defect_type_model, structural_unit_type_model  # no qa

MagnetogramDefect = sa.Table(
    "magnetogram_defect",
    base_alchemy_model.Base.metadata,
    sa.Column(
        "id",
        sa.UUID,
        primary_key=True,
        comment="Идентификатор связи",
        default=lambda: str(uuid.uuid4())
    ),
    sa.Column(
        "magnetogram_id",
        sa.UUID,
        sa.ForeignKey("magnetogram.id"),
        primary_key=True,
        comment="Идентификатор магнитограммы"
    ),
    sa.Column(
        "defect_id",
        sa.UUID,
        sa.ForeignKey("defect.id"),
        primary_key=True,
        comment="Идентификатор дефекта"
    )
)

MagnetogramStructuralUnit = sa.Table(
    "magnetogram_structural_unit",
    base_alchemy_model.Base.metadata,
    sa.Column(
        "id",
        sa.UUID,
        primary_key=True,
        comment="Идентификатор связи",
        default=lambda: str(uuid.uuid4())
    ),
    sa.Column(
        "magnetogram_id",
        sa.UUID,
        sa.ForeignKey("magnetogram.id"),
        primary_key=True,
        comment="Идентификатор магнитограммы"
    ),
    sa.Column(
        "structural_unit_id",
        sa.UUID,
        sa.ForeignKey("structural_unit.id"),
        primary_key=True,
        comment="Идентификатор структурного элемента"
    )
)


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
    defects: orm.Mapped[list[Defect]] = orm.relationship(
        secondary=MagnetogramDefect,
        back_populates="magnetograms",
        lazy="joined"
    )
    structural_units: orm.Mapped[list[StructuralUnit]] = orm.relationship(
        secondary=MagnetogramStructuralUnit,
        back_populates="magnetograms",
        lazy="joined"
    )
    history = orm.relationship("History", uselist=False, back_populates="magnetogram")


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
    type_id = sa.Column(sa.UUID, sa.ForeignKey("defect_type.id"), comment="Идентификатор типа дефекта")
    x_coord = sa.Column(sa.Integer, comment="Координата по оси X", nullable=False)
    continue_for = sa.Column(
        sa.Integer,
        comment="Количество таких же дефектов справа по оси X",
        default=0,
        nullable=False
    )
    type = orm.relationship("DefectType", back_populates="defects", lazy="joined")
    magnetograms: orm.Mapped[list[Magnetogram]] = orm.relationship(
        secondary=MagnetogramDefect,
        back_populates="defects",
        lazy="joined"
    )


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
    type_id = sa.Column(
        sa.UUID,
        sa.ForeignKey("structural_unit_type.id"),
        comment="Идентификатор типа структурного элемента"
    )
    x_coord = sa.Column(sa.Integer, comment="Координата по оси X", nullable=False)
    continue_for = sa.Column(
        sa.Integer,
        comment="Количество таких же структурных элементов справа по оси X",
        default=0,
        nullable=False
    )
    type = orm.relationship("StructuralUnitType", back_populates="structural_units", lazy="joined")
    magnetograms: orm.Mapped[list[Magnetogram]] = orm.relationship(
        secondary=MagnetogramStructuralUnit,
        back_populates="structural_units",
        lazy="joined"
    )
