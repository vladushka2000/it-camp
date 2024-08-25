import uuid

from pydantic import computed_field, Field

from interfaces import base_schema
from tools import enums, enum_utils


class Defect(base_schema.BaseSchema):
    """
    Модель дефекта
    """

    id: uuid.UUID = Field(description="Идентификатор дефекта")
    type_id: uuid.UUID = Field(description="Идентификатор типа дефекта")
    x_coord: int = Field(description="Координата по оси X")
    continue_for: int = Field(description="Количество таких же дефектов справа по оси X", default=0)

    @computed_field
    @property
    def type_name(self) -> enums.Defect:
        return enum_utils.EnumUtil.get_value_by_id(self.type_id, enums.Defect)
