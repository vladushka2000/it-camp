import uuid

from pydantic import Field

from interfaces import base_schema


class Defect(base_schema.BaseSchema):
    """
    Модель дефекта
    """

    id: uuid.UUID = Field(description="Идентификатор дефекта")
    type_id: uuid.UUID = Field(description="Идентификатор типа дефекта")
    type_name: str | None = Field(description="Название типа дефекта", default=None)
    x_coord: int = Field(description="Координата по оси X")
    continue_for: int = Field(description="Количество таких же дефектов справа по оси X", default=0)


class StructuralUnit(base_schema.BaseSchema):
    """
    Модель структурного элемента
    """

    id: uuid.UUID = Field(description="Идентификатор структурного элемента")
    type_id: uuid.UUID = Field(description="Идентификатор структурного элемента")
    type_name: str | None = Field(description="Название типа структурного элемента", default=None)
    x_coord: int = Field(description="Координата по оси X")
    continue_for: int = Field(description="Количество таких же структурных элементов справа по оси X", default=0)


class MagnetogramEdit(base_schema.BaseSchema):
    """
    Модель редактирования магнитограммы
    """

    new_defects: list[Defect] = Field(description="Список новых дефектов")
    new_structural_units: list[StructuralUnit] = Field(description="Список новых структруных элементов")


class Magnetogram(base_schema.BaseSchema):
    """
    Модель магнитограммы
    """

    user_name: str = Field(description="Имя пользователя", alias="userName")
    magnetogram: bytes = Field(description="Магнитограмма в формате pickle")
    object_name: str = Field(description="Название объекта", alias="objectName")
    comment: str | None = Field(description="Комментарий пользователя")


class MagnetogramToUpload(Magnetogram):
    """
    Модель магнитограммы для загрузки
    """

    pass
