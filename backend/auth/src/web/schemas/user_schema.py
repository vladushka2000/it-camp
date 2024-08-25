import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class UserInfoModel(base_schema.BaseSchema):
    """
    Модель информации о пользователе
    """

    id: uuid.UUID = Field(description="Идентификатор пользователя")
    name: str = Field(description="Имя пользователя", alias="name")
    role_id: uuid.UUID = Field(description="Идентификатор роли", alias="roleId")
    created_at: datetime.datetime = Field(description="Дата регистрации", alias="createdAt")
