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

    AIOHTTP_REPOSITORY = "aiohttp_repository"


class AuthEndpoints(enum.Enum):
    """
    Enum эндпоинтов сервиса Auth
    """

    SIGN_UP = "/auth/sign-up"
    SIGN_IN = "/auth/sign-in"
    REFRESH_TOKENS = "/auth/refresh-tokens"
    TOKEN_INFO = "/users/token-info"


class ReporterEndpoints(enum.Enum):
    """
    Enum эндпоинтов сервиса Reporter
    """

    CREATE = "/reporter/create"
    GET_REPORTS = "/reporter/reports"
    GET_REPORT = "/reporter/reports/{report_id}"


class ProcessorEndpoints(enum.Enum):
    """
    Enum эндпоинтов сервиса Processor
    """

    UPLOAD = "/processor/upload"
    GET_MAGNETOGRAM = "/processor/magnetograms/{magnetogram_id}"
    EDIT_MAGNETOGRAM = "/processor/magnetograms/{magnetogram_id}/edit"
    GET_HISTORY = "/processor/history"


class Role(base_enum.AbstractIdNameEnum):
    """
    Enum ролей пользователей
    """

    EXPERT = (uuid.UUID("f1ffeaba-e4ca-4c6b-91fc-2fcd004fb7ec"), "Expert")
