import datetime

from fastapi import APIRouter, Query

from services import history_service
from web.schemas import history_schema

router = APIRouter(prefix="/processor")


@router.get("/history")
async def get_history_records(
    date_from: datetime.datetime = Query(alias="dateFrom"),
    date_to: datetime.datetime = Query(alias="dateTo"),
) -> list[history_schema.History]:
    """
    Получить записи истории действий пользователей по датам их создания
    :param date_from: дата начала просмотра
    :param date_to: дата конца просмотра
    :return: записи истории
    """

    records = await history_service.HistoryService.get_history_records(date_from, date_to)

    return [
        history_schema.History(
            id=record.id,
            magnetogram_id=record.magnetogram_id,
            action_type_id=record.action_type_id,
            type_name=record.type_name,
            user_name=record.user_name,
            date=record.date
        ) for record in records
    ]
