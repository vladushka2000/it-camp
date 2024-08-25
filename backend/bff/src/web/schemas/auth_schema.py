from pydantic import Field

from interfaces import base_schema


class AuthModel(base_schema.BaseSchema):
    """
    Модель для регистрации и входа пользователя в систему
    """

    name: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")


class JWTModel(base_schema.BaseSchema):
    """
    Модель данных JWT-токенов
    """

    access_token: str = Field(description="Access-токен", alias="accessToken")
    refresh_token: str = Field(description="Refresh-токен", alias="refreshToken")
