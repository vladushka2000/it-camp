import uuid

from pydantic import field_validator, Field

from interfaces import base_schema
from tools import enums


class AuthDTO(base_schema.PydanticBase):
    """
    DTO, содержащий данные о регистрации пользователя
    """

    name: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")


class TokenAttrsDTO(base_schema.PydanticBase):
    """
    DTO, содержащий данные о параметрах токена
    """

    token_type: enums.TokenType = Field(description="Тип токена")


class TokensDTO(base_schema.PydanticBase):
    """
    DTO, содержащий данные о токенах пользователя
    """

    access_token: str = Field(description="Access-токен")
    refresh_token: str = Field(description="Refresh-токен")


class UsersRefreshToken(base_schema.PydanticBase):
    """
    DTO, содержащий информацию о пользователе и его refresh_токене
    """

    user_id: str = Field(description="Идентификатор пользователя")
    refresh_token: str = Field(description="Refresh-токен")

    @field_validator("user_id", mode="before")
    @classmethod
    def convert_user_id_to_str(cls, user_id: uuid.UUID) -> str:
        """
        Конвертировать идентификатор пользователя из UUID в строку
        """

        return str(user_id)
