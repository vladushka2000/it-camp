import datetime
import uuid

from dependency_injector.wiring import Provide
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_repository, base_service, base_uow, base_schema
from tools import di_container, exceptions
from dto import report_dto


class ReporterService(base_service.AbstractService):
    """
    Сервис для работы с отчетами
    """

    class _DIFactoriesObjectsDTO(base_schema.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        alchemy_session: AsyncSession = Field(description="Сессия Алхимии")

        report_repository: base_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с отчетами"
        )

        alchemy_uow: base_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Алхимии"
        )

    alchemy_session_factory = Provide[
        di_container.SessionContainer.alchemy_session_factory
    ]

    report_repository_factory = Provide[
        di_container.RepositoryContainer.report_repository_factory
    ]

    alchemy_uow_factory = Provide[di_container.UOWContainer.alchemy_uow_factory]

    @classmethod
    async def _get_di_objects(cls) -> _DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        async with cls.alchemy_session_factory.session_maker() as async_session:
            alchemy_session = async_session

        report_repository = cls.report_repository_factory.create(alchemy_session)

        alchemy_uow = cls.alchemy_uow_factory.create()
        alchemy_uow.add_repository(report_repository.name, report_repository)

        return cls._DIFactoriesObjectsDTO(
            alchemy_session=alchemy_session,
            report_repository=report_repository,
            alchemy_uow=alchemy_uow
        )

    @classmethod
    async def create_report(cls, report_info: report_dto.ReportDataDTO) -> None:
        """
        Выполнить логику создания отчета
        :param report_info: данные об отчете
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        repository = di_objects.report_repository

        async with uow:
            uow.repositories[repository.name].create(report_info)

            await uow.commit()

    @classmethod
    async def get_reports(
        cls,
        date_from: datetime.datetime,
        date_to: datetime.datetime
    ) -> list[report_dto.ReportDataMagnetogramInfoDTO]:
        """
        Выполнить логику получения отчетов по датам
        :param date_from: дата начала просмотра отчетов
        :param date_to: дата конца просмотра отчетов
        :return: отчеты
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        repository = di_objects.report_repository

        async with uow:
            reports = await uow.repositories[repository.name].retrieve(date_from=date_from, date_to=date_to)

        if reports is None:
            return []

        return reports

    @classmethod
    async def get_report(cls, report_id: uuid.UUID) -> report_dto.ReportDataMagnetogramInfoDTO:
        """
        Выполнить логику получения отчета по идентификатору
        :param report_id: идентификатор отчета
        :return: отчет
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        repository = di_objects.report_repository

        async with uow:
            result = await uow.repositories[repository.name].retrieve(report_id=report_id)

            if not result:
                raise exceptions.UserFaultException("Отчет не найден")

            [report] = result

        return report
