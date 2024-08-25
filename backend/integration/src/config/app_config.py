import dotenv
from pydantic import computed_field, Field, PostgresDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    """
    Класс настроек для работы сервиса
    """

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
