import enum
import uuid

from interfaces import base_enum


class TokenType(enum.Enum):
    """
    Enum типа токена
    """

    ACCESS = "access"
    REFRESH = "refresh"


class RepositoryName(enum.Enum):
    """
    Enum названий репозиториев
    """

    USER_REPOSITORY = "user_repository"
    TOKEN_REPOSITORY = "token_repository"


class PasswordHasherAlgorithm(enum.Enum):
    """
    Enum алгоритмов хеширования паролей
    """

    BCRYPT = "bcrypt"


class JWTAlgorithm(enum.Enum):
    """
    Enum алгоритмов хеширования jwt-токена
    """

    HS256 = "HS256"


class Role(base_enum.AbstractIdNameEnum):
    """
    Enum ролей пользователей
    """

    EXPERT = (uuid.UUID("f1ffeaba-e4ca-4c6b-91fc-2fcd004fb7ec"), "Expert")
