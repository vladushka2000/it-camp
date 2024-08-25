import datetime
import uuid

from fastapi import status, APIRouter, Query

from dto import report_dto
from services import reporter_service
from web.schemas import report_schema

router = APIRouter(prefix="/reporter")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_report(
    report: report_schema.ReportRequest,
) -> None:
    """
    Создать отчет
    :param report: данные об отчете
    """

    report_info = report_dto.ReportDataDTO(
        id=uuid.uuid4(),
        magnetogram_id=report.magnetogram_id,
        report=report.report,
        user_name=report.user_name,
        created_at=report.created_at
    )

    await reporter_service.ReporterService.create_report(report_info)


@router.get("/reports")
async def get_reports(
    date_from: datetime.datetime = Query(alias="dateFrom"),
    date_to: datetime.datetime = Query(alias="dateTo"),
) -> list[report_schema.ReportResponse]:
    """
    Получить отчеты по датам их создания
    :param date_from: дата начала просмотра отчетов
    :param date_to: дата конца просмотра отчетов
    :return: отчеты
    """

    reports = await reporter_service.ReporterService.get_reports(date_from, date_to)

    return [
        report_schema.ReportResponse(
            id=report.id,
            magnetogram_id=report.magnetogram_id,
            object_name=report.object_name,
            user_name=report.user_name,
            created_at=report.created_at
        )
        for report in reports
    ]


@router.get("/reports/{report_id}")
async def get_report(
    report_id: uuid.UUID
) -> report_schema.ReportObjectResponse:
    """
    Получить отчет по его идентификатору
    :param report_id: идентификатор отчета
    :return: отчет
    """

    report = await reporter_service.ReporterService.get_report(report_id)

    return report_schema.ReportObjectResponse(report=report.report)
