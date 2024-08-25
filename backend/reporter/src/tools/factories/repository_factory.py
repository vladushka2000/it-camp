from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_factory
from repositories import report_repository
from tools import enums


class ReportRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с отчетами
    """

    def create(self, session: AsyncSession) -> report_repository.ReportRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        :return: объект репозитория
        """

        return report_repository.ReportRepository(
            enums.RepositoryName.REPORT_REPOSITORY.value, session
        )
