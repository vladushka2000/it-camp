import dotenv
from pydantic import computed_field, Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    """
    Класс настроек для работы сервиса
    """

    app_name: str = Field(
        description="Название сервиса", default="BFF", alias="APP_NAME"
    )
    app_version: str = Field(
        description="Версия сервиса", default="1.0.0", alias="APP_VERSION"
    )
    app_host: str = Field(
        description="Адрес сервиса", default="0.0.0.0", alias="APP_HOST"
    )
    app_port: int = Field(description="Порт сервиса", default=7777, alias="APP_PORT")

    is_dev: bool = Field(
        description="Флаг о том, что приложение развернуто в режиме разработки",
        default=False,
        alias="IS_DEV",
    )

    service_url_string: str = Field(description="Шаблон URL-адреса сервисов", default="{schema}://{host}:{port}")

    auth_host: str = Field(description="Хост сервиса Auth", default="localhost", alias="AUTH_HOST")
    auth_port: int = Field(description="Порт сервиса Auth", default=7771, alias="AUTH_PORT")
    auth_schema: str = Field(description=" Схема URL", default="http", alias="AUTH_SCHEMA")

    reporter_host: str = Field(description="Хост сервиса Reporter", default="localhost", alias="REPORTER_HOST")
    reporter_port: int = Field(description="Порт сервиса Reporter", default=7772, alias="REPORTER_PORT")
    reporter_schema: str = Field(description=" Схема URL", default="http", alias="REPORTER_SCHEMA")

    processor_host: str = Field(description="Хост сервиса Processor", default="localhost", alias="PROCESSOR_HOST")
    processor_port: int = Field(description="Порт сервиса Processor", default=7773, alias="PROCESSOR_PORT")
    processor_schema: str = Field(description=" Схема URL", default="http", alias="PROCESSOR_SCHEMA")

    @computed_field
    @property
    def get_auth_host(self) -> str:
        return self.service_url_string.format(
            schema=self.auth_schema,
            host=self.auth_host,
            port=self.auth_port
        )

    @computed_field
    @property
    def get_reporter_host(self) -> str:
        return self.service_url_string.format(
            schema=self.reporter_schema,
            host=self.reporter_host,
            port=self.reporter_port
        )

    @computed_field
    @property
    def get_processor_host(self) -> str:
        return self.service_url_string.format(
            schema=self.processor_schema,
            host=self.processor_host,
            port=self.processor_port
        )


config = Config()
