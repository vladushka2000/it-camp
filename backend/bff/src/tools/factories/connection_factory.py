import aiohttp

from interfaces import base_factory


class HTTPSessionFactory(base_factory.AbstractFactory):
    """
    Фабрика асинхронных HTTP-сессий
    """

    def create(self) -> aiohttp.ClientSession:
        """
        Создать сессию
        :return: сессия
        """

        return aiohttp.ClientSession()
