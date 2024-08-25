import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class UserDataDTO(base_schema.BaseSchema):
    """
    DTO, содержащий информацию о пользователе
    """

    user_id: uuid.UUID = Field(description="Идентификатор пользователя", alias="userId")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    role_id: uuid.UUID = Field(description="Роль пользователя", alias="roleId")
    created_at: datetime.datetime = Field(description="Дата регистрации", alias="createdAt")
