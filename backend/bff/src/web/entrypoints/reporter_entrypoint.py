import base64
import datetime
import io
import uuid

from fastapi import status, APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from dto import report_dto
from services import reporter_service
from tools import enums
from web.dependencies import token_dependency
from web.schemas import report_schema

router = APIRouter(prefix="/reporter")


@router.post("/create")
async def create_report(
    report: report_schema.ReportRequest,
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> StreamingResponse:
    """
    Создать отчет
    :param report: информация об отчете
    :param role: роль пользователя
    :return: загрузка отчета
    """

    report_data = report_dto.ReportDataDTO(
        magnetogram_id=report.magnetogram_id,
        report=report.report,
        user_name=report.user_name,
        created_at=datetime.datetime.now()
    )

    result = await reporter_service.ReporterService.create_report(report_data)

    if result.status == status.HTTP_201_CREATED:
        pdf_io = io.BytesIO(base64.b64decode(report.report))

        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=output.pdf"
            }
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.get("/reports")
async def get_reports(
    date_from: datetime.datetime = Query(alias="dateFrom"),
    date_to: datetime.datetime = Query(alias="dateTo"),
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> list[report_schema.ReportResponse]:
    """
    Получить отчеты
    :param date_from: дата начала просмотра отчетов
    :param date_to: дата конца просмотра отчетов
    :param role: роль пользователя
    :return: список отчетов
    """

    result = await reporter_service.ReporterService.get_reports(date_from, date_to)

    if result.status == status.HTTP_200_OK:
        return [
            report_schema.ReportResponse(
                id=report["id"],
                magnetogram_id=report["magnetogramId"],
                object_name=report["objectName"],
                user_name=report["userName"],
                created_at=report["createdAt"]
            )
            for report in result.payload
        ]

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.get("/reports/{report_id}")
async def get_report(
    report_id: uuid.UUID,
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> StreamingResponse:
    """
    Получить отчет
    :param report_id: идентификатор отчета
    :param role: роль пользователя
    :return: отчет
    """

    result = await reporter_service.ReporterService.get_report(report_id)

    if result.status == status.HTTP_200_OK:
        pdf_io = io.BytesIO(base64.b64decode(result.payload["report"]))

        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=output.pdf"
            }
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )
