import datetime

from dependency_injector.wiring import Provide
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_repository, base_uow, base_util, base_processor, base_schema, base_service
from tools import di_container
from dto import history_dto


class HistoryService(base_service.AbstractService):
    """
    Сервис для работы с магнитограммами
    """

    class _DIFactoriesObjectsDTO(base_schema.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        alchemy_session: AsyncSession = Field(description="Сессия Алхимии")

        magnetogram_repository: base_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с магнитограммами"
        )
        history_repository: base_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с историей загрузок"
        )

        alchemy_uow: base_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Алхимии"
        )

        processor: base_processor.AbstractProcessor = Field(
            description="Обработчик магнитограммы"
        )
        truncator: base_util.AbstractUtil = Field(description="Форматтер результата обработчика")

    alchemy_session_factory = Provide[
        di_container.SessionContainer.alchemy_session_factory
    ]

    magnetogram_repository_factory = Provide[
        di_container.RepositoryContainer.magnetogram_repository_factory
    ]
    history_repository_factory = Provide[
        di_container.RepositoryContainer.history_repository_factory
    ]

    alchemy_uow_factory = Provide[di_container.UOWContainer.alchemy_uow_factory]

    processor_factory = Provide[di_container.ToolsContainer.processor_factory]
    truncator_factory = Provide[di_container.ToolsContainer.truncator_factory]

    @classmethod
    async def _get_di_objects(cls) -> _DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        async with cls.alchemy_session_factory.session_maker() as async_session:
            alchemy_session = async_session

        magnetogram_repository = cls.magnetogram_repository_factory.create(alchemy_session)
        history_repository = cls.history_repository_factory.create(alchemy_session)

        alchemy_uow = cls.alchemy_uow_factory.create()
        alchemy_uow.add_repository(magnetogram_repository.name, magnetogram_repository)
        alchemy_uow.add_repository(history_repository.name, history_repository)

        processor = cls.processor_factory.create()
        truncator = cls.truncator_factory.create()

        return cls._DIFactoriesObjectsDTO(
            alchemy_session=alchemy_session,
            magnetogram_repository=magnetogram_repository,
            history_repository=history_repository,
            alchemy_uow=alchemy_uow,
            processor=processor,
            truncator=truncator
        )

    @classmethod
    async def get_history_records(
        cls,
        date_from: datetime.datetime,
        date_to: datetime.datetime
    ) -> list[history_dto.HistoryDTO]:
        """
        Выполнить логику получения записей истории по датам
        :param date_from: дата начала просмотра
        :param date_to: дата конца просмотра
        :return: записи истории
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        repository = di_objects.history_repository

        async with uow:
            records = await uow.repositories[repository.name].retrieve(date_from=date_from, date_to=date_to)

        if records is None:
            return []

        return records
