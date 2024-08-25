import base64
import datetime
import uuid

from dependency_injector.wiring import Provide
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_repository, base_uow, base_util, base_processor, base_schema, base_service
from tools import di_container, enums
from dto import defect_dto, history_dto, magnetogram_dto, structural_unit_dto


class ProcessorService(base_service.AbstractService):
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
    async def upload_magnetogram(
        cls,
        magnetogram: magnetogram_dto.MagnetogramToProcess
    ) -> magnetogram_dto.MagnetogramProcessed:
        """
        Выполнить логику обработки магнитограммы
        :param magnetogram: объект магнитограммы
        :return: данные обработанной магнитограммы
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        magnetogram_repository = di_objects.magnetogram_repository
        history_repository = di_objects.history_repository
        processor = di_objects.processor
        truncator = di_objects.truncator

        async with uow:
            processor.magnetogram_pickle = base64.b64decode(magnetogram.magnetogram)
            processor_result = processor.process()

            formatted_defects = truncator.truncate_process_result(processor_result.defects)
            formatted_structural_units = truncator.truncate_process_result(processor_result.structural_units)

            processed_image = processor.get_processed_image()

            processed_magnetogram = magnetogram_dto.MagnetogramProcessed(
                id=magnetogram.id,
                user_name=magnetogram.user_name,
                object_name=magnetogram.object_name,
                comment=magnetogram.comment,
                created_at=magnetogram.created_at,
                magnetogram=processed_image
            )

            history_record = history_dto.HistoryDTO(
                id=uuid.uuid4(),
                magnetogram_id=magnetogram.id,
                action_type_id=enums.HistoryAction.UPLOAD.id,
                user_name=magnetogram.user_name,
                date=magnetogram.created_at
            )

            await uow.repositories[magnetogram_repository.name].create(
                processed_magnetogram,
                formatted_defects,
                formatted_structural_units
            )

            uow.repositories[history_repository.name].create(history_record)

            await uow.commit()

        return magnetogram_dto.MagnetogramProcessed(
            id=magnetogram.id,
            user_name=magnetogram.user_name,
            object_name=magnetogram.object_name,
            comment=magnetogram.comment,
            created_at=magnetogram.created_at,
            structural_units=formatted_structural_units,
            defects=formatted_defects,
            magnetogram=processed_image
        )

    @classmethod
    async def edit_magnetogram(
        cls,
        magnetogram_id: uuid.UUID,
        new_defects: list[defect_dto.Defect],
        new_structural_units: list[structural_unit_dto.StructuralUnit]
    ) -> None:
        """
        Выполнить логику обработки магнитограммы
        :param magnetogram_id: идентификатор магнитограммы
        :param new_defects: новые дефекты
        :param new_structural_units: новые структруные элементы
        :return: данные обработанной магнитограммы
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        magnetogram_repository = di_objects.magnetogram_repository
        history_repository = di_objects.history_repository

        async with uow:
            await uow.repositories[magnetogram_repository.name].delete(magnetogram_id)
            magnetogram_db_model = await uow.repositories[magnetogram_repository.name].retrieve(magnetogram_id)

            magnetogram = magnetogram_dto.MagnetogramProcessed(
                id=magnetogram_db_model.id,
                user_name=magnetogram_db_model.user_name,
                object_name=magnetogram_db_model.object_name,
                comment=magnetogram_db_model.comment,
                created_at=magnetogram_db_model.created_at,
                structural_units=new_structural_units,
                defects=new_defects,
                magnetogram=magnetogram_db_model.magnetogram
            )

            history_record = history_dto.HistoryDTO(
                id=uuid.uuid4(),
                magnetogram_id=magnetogram.id,
                action_type_id=enums.HistoryAction.EDIT.id,
                user_name=magnetogram.user_name,
                date=datetime.datetime.now()
            )

            await uow.repositories[magnetogram_repository.name].update(
                magnetogram_db_model,
                new_defects,
                new_structural_units
            )

            uow.repositories[history_repository.name].create(history_record)

            await uow.commit()

    @classmethod
    async def get_magnetogram(cls, magnetogram_id: uuid.UUID) -> magnetogram_dto.MagnetogramProcessed:
        """
        Выполнить логику получения магнитограммы
        :param magnetogram_id: идентификатор магнитограммы
        :return: данные обработанной магнитограммы
        """

        di_objects = await cls._get_di_objects()
        uow = di_objects.alchemy_uow
        repository = di_objects.magnetogram_repository
        truncator = di_objects.truncator

        async with uow:
            magnetogram = await uow.repositories[repository.name].retrieve_dto(magnetogram_id)

            formatted_defects = truncator.truncate_process_result(magnetogram.defects)
            formatted_structural_units = truncator.truncate_process_result(magnetogram.structural_units)

            return magnetogram_dto.MagnetogramProcessed(
                id=magnetogram.id,
                user_name=magnetogram.user_name,
                object_name=magnetogram.object_name,
                comment=magnetogram.comment,
                created_at=magnetogram.created_at,
                structural_units=formatted_structural_units,
                defects=formatted_defects,
                magnetogram=magnetogram.magnetogram
            )
