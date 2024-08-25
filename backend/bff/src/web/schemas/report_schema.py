import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class ReportModel(base_schema.BaseSchema):
    """
    Модель для создания отчета
    """

    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    user_name: str = Field(description="Имя пользователя", alias="userName")


class ReportRequest(ReportModel):
    """
    Модель для создания отчета
    """

    report: bytes = Field(description="Отчет в формате байтовой строки")


class ReportResponse(ReportModel):
    """
    Модель с данными об отчете
    """

    id: uuid.UUID = Field(description="Идентификатор отчета")
    created_at: datetime.datetime = Field(description="Дата создания", alias="createdAt")
    object_name: str = Field(description="Название объекта", alias="objectName")
