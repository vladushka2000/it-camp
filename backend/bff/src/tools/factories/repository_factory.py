import aiohttp

from interfaces import base_factory
from tools import enums
from repositories import (
    aiohttp_repository
)


class HTTPRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с пользователями
    """

    def create(self, session: aiohttp.ClientSession) -> aiohttp_repository.AIOHTTPRepository:
        """
        Создать объект репозитория
        :param session: HTTP-сессия
        """

        return aiohttp_repository.AIOHTTPRepository(
            enums.RepositoryName.AIOHTTP_REPOSITORY.value, session
        )
