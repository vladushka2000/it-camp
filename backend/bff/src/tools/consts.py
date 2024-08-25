from config import app_config
from dto import auth_dto
from tools import enums

config = app_config.config


class Auth:
    """
    Константы, связанные с аутентификацией
    """

    ACCESS_TOKEN_ATTRS = auth_dto.TokenAttrsDTO(token_type=enums.TokenType.ACCESS)
    REFRESH_TOKEN_ATTRS = auth_dto.TokenAttrsDTO(token_type=enums.TokenType.REFRESH)


class Time:
    """
    Константы, связанные с временем
    """

    STR_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
