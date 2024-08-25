import datetime
import uuid

import aiohttp
from dependency_injector.wiring import Provide
from pydantic import Field

from config import app_config
from interfaces import base_repository, base_schema, base_service
from tools import consts, di_container, enums
from dto import http_dto, report_dto


config = app_config.config


class ReporterService(base_service.AbstractService):
    """
    Сервис для работы с отчетами
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
    async def create_report(cls, report_info: report_dto.ReportDataDTO) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику создания отчета
        :param report_info: информация об отчете
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_reporter_host}{enums.ReporterEndpoints.CREATE.value}",
            payload={
                "magnetogramId": report_info.magnetogram_id,
                "report": report_info.report,
                "userName": report_info.user_name,
                "createdAt": report_info.created_at
            }
        )

        return await http_repository.create(http_request)

    @classmethod
    async def get_reports(
        cls,
        date_from: datetime.datetime,
        date_to: datetime.datetime
    ) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику получения отчетов
        :param date_from: дата начала просмотра отчетов
        :param date_to: дата конца просмотра отчетов
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_reporter_host}{enums.ReporterEndpoints.GET_REPORTS.value}",
            query_params={
                "dateFrom": date_from.strftime(consts.Time.STR_TIME_FORMAT),
                "dateTo": date_to.strftime(consts.Time.STR_TIME_FORMAT)
            }
        )

        return await http_repository.retrieve(http_request)

    @classmethod
    async def get_report(
        cls,
        report_id: uuid.UUID
    ) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику получения отчета
        :param report_id: идентификатор отчета
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_reporter_host}{enums.ReporterEndpoints.GET_REPORT.value.format(report_id=report_id)}"
        )

        return await http_repository.retrieve(http_request)
