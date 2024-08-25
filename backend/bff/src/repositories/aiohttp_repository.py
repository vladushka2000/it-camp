import aiohttp

from dto import http_dto
from interfaces import base_repository


class AIOHTTPRepository(
    base_repository.AbstractRepository,
    base_repository.CreateMixin,
    base_repository.RetrieveMixin,
    base_repository.UpdateMixin
):
    """
    Репозиторий для работы с HTTP-запросами
    """

    def __init__(self, name: str, session: aiohttp.ClientSession) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param session: http-сессия
        """

        self.session = session

        super().__init__(name)

    async def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            async with self.session.post(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            ) as response:
                result = await response.json()

                return http_dto.HTTPResponseDTO(
                    status=response.status,
                    payload=result
                )
        except aiohttp.ClientError as error:
            raise error
        finally:
            await self.session.close()

    async def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            async with self.session.get(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params
            ) as response:
                result = await response.json()

                return http_dto.HTTPResponseDTO(
                    status=response.status,
                    payload=result
                )
        except aiohttp.ClientError as error:
            raise error
        finally:
            await self.session.close()

    async def update(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            async with self.session.patch(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            ) as response:
                result = await response.json()

                return http_dto.HTTPResponseDTO(
                    status=response.status,
                    payload=result
                )
        except aiohttp.ClientError as error:
            raise error
        finally:
            await self.session.close()
