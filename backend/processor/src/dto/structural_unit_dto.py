import uuid

from pydantic import computed_field, Field

from interfaces import base_schema
from tools import enums, enum_utils


class StructuralUnit(base_schema.BaseSchema):
    """
    Модель структурного элемента
    """

    id: uuid.UUID = Field(description="Идентификатор структурного элемента")
    type_id: uuid.UUID = Field(description="Идентификатор структурного элемента")
    x_coord: int = Field(description="Координата по оси X")
    continue_for: int = Field(description="Количество таких же структурных элементов справа по оси X", default=0)

    @computed_field
    @property
    def type_name(self) -> enums.StructuralUnit:
        return enum_utils.EnumUtil.get_value_by_id(self.type_id, enums.StructuralUnit)
