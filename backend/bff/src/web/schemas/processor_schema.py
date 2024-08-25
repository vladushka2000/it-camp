import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class Defect(base_schema.BaseSchema):
    """
    Модель дефекта
    """

    type_id: uuid.UUID = Field(description="Идентификатор типа дефекта", alias="typeId")
    x_coord: int = Field(description="Координата по оси X", alias="xCoord")
    continue_for: int = Field(
        description="Количество таких же дефектов справа по оси X",
        default=0,
        alias="continueFor"
    )


class DefectRequest(Defect):
    """
    Модель дефекта для запроса
    """

    pass


class DefectResponse(Defect):
    """
    Модель дефекта для ответа
    """

    id: uuid.UUID = Field(description="Идентификатор дефекта")
    type_name: str = Field(description="Название типа дефекта", alias="typeName")


class StructuralUnit(base_schema.BaseSchema):
    """
    Модель структурного элемента
    """

    type_id: uuid.UUID = Field(description="Идентификатор типа структурного элемента", alias="typeId")
    x_coord: int = Field(description="Координата по оси X", alias="xCoord")
    continue_for: int = Field(
        description="Количество таких же структурных элементов справа по оси X",
        default=0,
        alias="continueFor"
    )


class StructuralUnitRequest(StructuralUnit):
    """
    Модель структурного элемента для запроса
    """

    pass


class StructuralUnitResponse(StructuralUnit):
    """
    Модель структурного элемента для ответа
    """

    id: uuid.UUID = Field(description="Идентификатор дефекта")
    type_name: str = Field(description="Название типа структурного элемента", alias="typeName")


class MagnetogramEditRequest(base_schema.BaseSchema):
    """
    Модель редактирования магнитограммы
    """

    new_defects: list[DefectRequest] = Field(description="Список новых дефектов", alias="newDefects")
    new_structural_units: list[StructuralUnitRequest] = Field(
        description="Список новых структруных элементов",
        alias="newStructuralUnits"
    )


class Magnetogram(base_schema.BaseSchema):
    """
    Модель для магнитограммы
    """

    user_name: str = Field(description="Имя пользователя", alias="userName")
    object_name: str = Field(description="Название объекта", alias="objectName")
    magnetogram: bytes = Field(description="Магнитограмма в формате pickle")
    comment: str | None = Field(description="Комментарий пользователя", default=None)


class MagnetogramRequest(Magnetogram):
    """
    Модель для загрузки магнитограммы
    """

    pass


class MagnetogramResponse(MagnetogramRequest):
    """
    Модель, содержащая данные загруженной магнитограммы
    """

    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    magnetogram: bytes = Field(description="Магнитограмма в формате png")
    structural_units: list[StructuralUnitResponse] = Field(
        description="Список структурных элементов",
        alias="structuralUnits"
    )
    defects: list[DefectResponse] = Field(description="Список дефектов")
    created_at: datetime.datetime = Field(description="Дата создания магнитограммы", alias="createdAt")


class History(base_schema.BaseSchema):
    """
    Модель для записей истории действий пользователей
    """

    id: uuid.UUID = Field(description="Идентификатор записи")
    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    action_type_id: uuid.UUID = Field(description="Идентификатор действия пользователя", alias="actionTypeId")
    type_name: str = Field(description="Название действия пользователя", alias="typeName")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    date: datetime.datetime = Field(description="Дата")
