import dotenv
from pydantic import computed_field, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

from tools import enums

dotenv.load_dotenv()


class Config(BaseSettings):
    """
    Класс настроек для работы сервиса
    """

    app_name: str = Field(
        description="Название сервиса", default="Auth", alias="APP_NAME"
    )
    app_version: str = Field(
        description="Версия сервиса", default="1.0.0", alias="APP_VERSION"
    )
    app_host: str = Field(
        description="Адрес сервиса", default="0.0.0.0", alias="APP_HOST"
    )
    app_port: int = Field(description="Порт сервиса", default=7771, alias="APP_PORT")

    is_dev: bool = Field(
        description="Флаг о том, что приложение развернуто в режиме разработки",
        default=False,
        alias="IS_DEV",
    )

    secret_key: str = Field(description="Секретный ключ", alias="SECRET_KEY")
    jwt_algorithm: enums.JWTAlgorithm = Field(
        description="Алгоритм кодирования jwt-токенов",
        default=enums.JWTAlgorithm.HS256.value,
        alias="JWT_ALGORITHM",
    )
    access_token_expire_in_sec: int = Field(
        description="Время жизни access-токена в секундах",
        alias="ACCESS_TOKEN_EXPIRATION_IN_SEC",
    )
    refresh_token_expire_in_sec: int = Field(
        description="Время жизни refresh-токена в секундах",
        alias="REFRESH_TOKEN_EXPIRATION_IN_SEC",
    )

    postgres_username: str = Field(
        description="Имя пользователя БД Postgres", default="admin", alias="PG_USERNAME"
    )
    postgres_password: str = Field(
        description="Пароль пользователя БД Postgres", default="admin", alias="PG_PASSWORD"
    )
    postgres_host: str = Field(
        description="Хост БД Postgres", default="localhost", alias="PG_HOST"
    )
    postgres_port: int = Field(
        description="Порт БД Postgres", default=5431, alias="PG_PORT"
    )
    postgres_database: str = Field(
        description="Название БД Postgres",
        default="auth",
        alias="PG_DB_NAME",
    )
    postgres_scheme: str = Field(
        description="Схема URL БД Postgres",
        default="postgresql+asyncpg",
        alias="PG_URL_SCHEME",
    )

    redis_token_host: str = Field(
        escription="Хост Redis для хранения токенов",
        default="localhost",
        alias="REDIS_TOKEN_HOST",
    )
    redis_token_port: int = Field(
        escription="Порт Redis для хранения токенов",
        default=6378,
        alias="REDIS_TOKEN_PORT",
    )
    redis_scheme: str = Field(
        description="Схема URL БД Redis", default="redis", alias="REDIS_URL_SCHEME"
    )

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        """
        Собрать Postgres DSN
        """

        return PostgresDsn.build(
            scheme=self.postgres_scheme,
            username=self.postgres_username,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_database
        )

    @computed_field
    @property
    def redis_token_dsn(self) -> RedisDsn:
        """
        Собрать Redis DSN для работы с токенами
        """

        return RedisDsn.build(
            scheme=self.redis_scheme,
            host=self.redis_token_host,
            port=self.redis_token_port,
        )


config = Config()
