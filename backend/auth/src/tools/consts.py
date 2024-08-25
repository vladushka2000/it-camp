from config import app_config
from dto import auth_dto
from tools import enums

config = app_config.config


class Auth:
    """
    Константы, связанные с аутентификацией
    """

    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 5
    MAX_PASSWORD_LENGTH = 20

    ACCESS_TOKEN_ATTRS = auth_dto.TokenAttrsDTO(
        token_type=enums.TokenType.ACCESS,
        expiration_time_in_sec=config.access_token_expire_in_sec,
    )
    REFRESH_TOKEN_ATTRS = auth_dto.TokenAttrsDTO(
        token_type=enums.TokenType.REFRESH,
        expiration_time_in_sec=config.refresh_token_expire_in_sec,
    )
