import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class UserDTOBase(base_schema.BaseSchema):
    """
    Базовый DTO, содержащий информацию о пользователе
    """

    id: uuid.UUID = Field(
        description="Идентификатор пользователя", default=uuid.uuid4()
    )
    name: str = Field(description="Имя пользователя")
    role: uuid.UUID = Field(description="Идентификатор роли пользователя")
    created_at: datetime.datetime = Field(description="Дата регистрации", alias="createdAt")


class UserDTO(UserDTOBase):
    """
    DTO, содержащий все данные о пользователе
    """

    password: str = Field(description="Пароль")
