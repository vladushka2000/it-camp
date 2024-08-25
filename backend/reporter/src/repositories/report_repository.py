import datetime
import uuid

from sqlalchemy import select, and_

from dto import report_dto
from interfaces import base_repository
from repositories.models import magnetogram_model, report_model


class ReportRepository(
    base_repository.AbstractAlchemyRepository, base_repository.CreateMixin, base_repository.RetrieveMixin
):
    """
    Репозиторий для работы с отчетами
    """

    def create(self, report: report_dto.ReportDataDTO) -> None:
        """
        Создать запись отчета
        :param report: объект отчета
        """

        report_db_model = report_model.Report(
            id=str(report.id),
            magnetogram_id=str(report.magnetogram_id),
            user_name=report.user_name,
            report=report.report,
            created_at=report.created_at,
        )

        self.session.add(report_db_model)

    async def retrieve(
        self,
        date_to: datetime.datetime | None = None,
        date_from: datetime.datetime | None = None,
        report_id: uuid.UUID | None = None
    ) -> list[report_dto.ReportDataMagnetogramInfoDTO] | None:
        """
        Получить запись отчета
        :param date_to: дата конца поиска
        :param date_from: дата начала поиска
        :param report_id: идентификатор отчета
        :return: список отчетов
        """

        query = (
            select(report_model.Report).
            join(magnetogram_model.Magnetogram)
        )

        filter_criteries = (
            report_model.Report.created_at >= date_from if (date_from and not report_id) else None,
            report_model.Report.created_at <= date_to if (date_to and not report_id) else None,
            report_model.Report.id == report_id if report_id else None
        )
        filter_criteries = [criteria for criteria in filter_criteries if criteria is not None]

        if len(filter_criteries) != 0:
            query = query.filter(
                and_(*filter_criteries)
            )

        result = await self.session.execute(query)
        result = result.scalars().all()

        if not result:
            return

        return [
            report_dto.ReportDataMagnetogramInfoDTO(
                id=report.id,
                magnetogram_id=report.magnetogram_id,
                object_name=report.magnetogram.object_name,
                user_name=report.user_name,
                report=report.report,
                created_at=report.created_at
            )
            for report in result
        ]
