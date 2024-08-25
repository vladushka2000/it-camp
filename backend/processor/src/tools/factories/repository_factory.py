from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_factory
from repositories import history_repository, magnetogram_repository
from tools import enums


class MagnetogramRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с магнитограммами
    """

    def create(self, session: AsyncSession) -> magnetogram_repository.MagnetogramRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        :return: объект репозитория
        """

        return magnetogram_repository.MagnetogramRepository(
            enums.RepositoryName.MAGNETOGRAM_REPOSITORY.value, session
        )


class HistoryRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с историей загрузок
    """

    def create(self, session: AsyncSession) -> history_repository.HistoryRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        :return: объект репозитория
        """

        return history_repository.HistoryRepository(
            enums.RepositoryName.HISTORY_REPOSITORY.value, session
        )
