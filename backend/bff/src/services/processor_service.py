import datetime
import uuid

import aiohttp
from dependency_injector.wiring import Provide
from pydantic import Field

from config import app_config
from interfaces import base_repository, base_schema, base_service
from tools import consts, di_container, enums
from dto import http_dto, processor_dto


config = app_config.config


class ProcessorService(base_service.AbstractService):
    """
    Сервис для работы с обработчиком
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
    async def upload_magnetogram(cls, magnetogram_info: processor_dto.MagnetogramToUpload) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику загрузки магнитограммы
        :param magnetogram_info: информация о магнитограмме
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_processor_host}{enums.ProcessorEndpoints.UPLOAD.value}",
            payload={
                "userName": magnetogram_info.user_name,
                "objectName": magnetogram_info.object_name,
                "magnetogram": magnetogram_info.magnetogram.decode("utf-8"),
                "comment": magnetogram_info.comment
            }
        )

        return await http_repository.create(http_request)

    @classmethod
    async def get_magnetogram(
        cls,
        magnetogram_id: uuid.UUID
    ) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику получения магнитограммы
        :param magnetogram_id: идентификатор магнитограммы
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_processor_host}"
                f"{enums.ProcessorEndpoints.GET_MAGNETOGRAM.value.format(magnetogram_id=magnetogram_id)}"
        )

        return await http_repository.retrieve(http_request)

    @classmethod
    async def edit_magnetogram(
        cls,
        magnetogram_id: uuid.UUID,
        edit_info: processor_dto.MagnetogramEdit
    ) -> http_dto.HTTPResponseDTO:
        """
        Выполнить логику получения отчета
        :param magnetogram_id: идентификатор магнитограммы
        :param edit_info: данные для обновления
        :return: объект ответа сервера
        """

        di_objects = await cls._get_di_objects()
        http_repository = di_objects.http_repository

        http_request = http_dto.HTTPRequestDTO(
            url=f"{config.get_processor_host}"
                f"{enums.ProcessorEndpoints.EDIT_MAGNETOGRAM.value.format(magnetogram_id=magnetogram_id)}",
            payload={
                "newDefects": [
                    {
                        "typeId": str(defect.type_id),
                        "xCoord": defect.x_coord,
                    } for defect in edit_info.new_defects
                ],
                "newStructuralUnits": [
                    {
                        "typeId": str(structural_unit.type_id),
                        "xCoord": structural_unit.x_coord
                    } for structural_unit in edit_info.new_structural_units
                ]
            }

        )

        return await http_repository.update(http_request)

    @classmethod
    async def get_history(
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
            url=f"{config.get_processor_host}{enums.ProcessorEndpoints.GET_HISTORY.value}",
            query_params={
                "dateFrom": date_from.strftime(consts.Time.STR_TIME_FORMAT),
                "dateTo": date_to.strftime(consts.Time.STR_TIME_FORMAT)
            }
        )

        return await http_repository.retrieve(http_request)
