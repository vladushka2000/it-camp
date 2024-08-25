import dotenv
from pydantic import computed_field, Field, PostgresDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    """
    Класс настроек для работы сервиса
    """

    app_name: str = Field(
        description="Название сервиса", default="Reporter", alias="APP_NAME"
    )
    app_version: str = Field(
        description="Версия сервиса", default="1.0.0", alias="APP_VERSION"
    )
    app_host: str = Field(
        description="Адрес сервиса", default="0.0.0.0", alias="APP_HOST"
    )
    app_port: int = Field(description="Порт сервиса", default=7772, alias="APP_PORT")

    is_dev: bool = Field(
        description="Флаг о том, что приложение развернуто в режиме разработки",
        default=False,
        alias="IS_DEV",
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
        description="Порт БД Postgres", default=5432, alias="PG_PORT"
    )
    postgres_database: str = Field(
        description="Название БД Postgres",
        default="magnetogram",
        alias="PG_DB_NAME",
    )
    postgres_scheme: str = Field(
        description="Схема URL БД Postgres",
        default="postgresql+asyncpg",
        alias="PG_URL_SCHEME",
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
            path=self.postgres_database,
        )


config = Config()
