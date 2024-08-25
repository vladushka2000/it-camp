import datetime
import uuid

from pydantic import Field

from interfaces import base_schema
from tools import enums


class History(base_schema.BaseSchema):
    """
    Модель для записей истории действий пользователей
    """

    id: uuid.UUID = Field(description="Идентификатор записи")
    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    action_type_id: uuid.UUID = Field(description="Идентификатор действия пользователя", alias="actionTypeId")
    type_name: enums.HistoryAction = Field(description="Название действия пользователя", alias="typeName")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    date: datetime.datetime = Field(description="Дата")
