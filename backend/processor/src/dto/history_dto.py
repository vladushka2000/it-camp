import datetime
import uuid

from pydantic import Field, computed_field

from interfaces import base_schema
from tools import enums, enum_utils


class HistoryDTO(base_schema.BaseSchema):
    """
    DTO, содержащий информацию об истории загрузок
    """

    id: uuid.UUID = Field(description="Идентификатор записи")
    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы")
    action_type_id: uuid.UUID = Field(description="Идентификатор действия пользователя")
    user_name: str = Field(description="Имя пользователя")
    date: datetime.datetime = Field(description="Дата", default=datetime.datetime.now())

    @computed_field
    @property
    def type_name(self) -> enums.HistoryAction:
        return enum_utils.EnumUtil.get_value_by_id(self.action_type_id, enums.HistoryAction)
