import datetime
import uuid

from pydantic import Field

from dto import defect_dto, structural_unit_dto
from interfaces import base_schema


class Magnetogram(base_schema.BaseSchema):
    """
    Модель магнитограммы
    """

    id: uuid.UUID = Field(description="Идентификатор магнитограммы")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    object_name: str = Field(description="Название объекта", alias="objectName")
    comment: str | None = Field(description="Комментарий пользователя")
    created_at: datetime.datetime = Field(description="Дата создания магнитограммы")


class MagnetogramToProcess(Magnetogram):
    """
    Модель магнитограммы для обработки
    """

    magnetogram: bytes = Field(description="Магнитограмма в формате pickle")


class MagnetogramWithElements(Magnetogram):
    """
    Модель обработанной магнитограммы
    """

    structural_units: list[structural_unit_dto.StructuralUnit] | None = Field(
        description="Список структурных элементов",
        default=None
    )
    defects: list[defect_dto.Defect] | None = Field(
        description="Список дефектов",
        default=None
    )
    magnetogram: bytes = Field(description="Магнитограмма в формате png")


class MagnetogramProcessed(MagnetogramWithElements):
    """
    Модель обработанной магнитограммы
    """

    magnetogram: bytes = Field(description="Магнитограмма в формате png")
