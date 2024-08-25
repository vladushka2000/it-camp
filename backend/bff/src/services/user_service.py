import aiohttp
from dependency_injector.wiring import Provide
from pydantic import Field

from config import app_config
from interfaces import base_repository, base_schema, base_service
from tools import di_container, enums
from dto import http_dto


config = app_config.config


class UserService(base_service.AbstractService):
    """
    Сервис для работы с логикой взаимодействия с данными пользователя
    """

    class _DIFactoriesObjectsDTO(base_schema.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        http_session: aiohttp.ClientSession = Field(description="HTTP-сессия")
        http_repository: base_repository.AbstractRepository = Field(description="HTTP-репозиторий")

    http_session_factory = Provide[
        di_container.SessionContainer.http_session_factory
    ]
    http_repository_factory = Provide[
        di_container.RepositoryContainer.http_repository_factory
    ]

    @classmethod
    async def _get_di_objects(cls) -> _DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        http_session = cls.http_session_factory.create()
        http_repository = cls.http_repository_factory.create(http_session)

        return cls._DIFactoriesObjectsDTO(http_session=http_session, http_repository=http_repository)

    @classmethod
    async def get_user_info_by_token(cls, token: str) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику получения данных о пользователе
        :param token: токен пользователя
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_auth_host}{enums.AuthEndpoints.TOKEN_INFO.value}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        return await http_repository.retrieve(http_request)
