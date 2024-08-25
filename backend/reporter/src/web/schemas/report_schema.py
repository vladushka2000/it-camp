import datetime
import uuid

from pydantic import field_validator, Field

from interfaces import base_schema


class ReportRequest(base_schema.BaseSchema):
    """
    Модель для создания отчета
    """

    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    report: bytes = Field(description="Отчет в формате байтовой строки")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    created_at: datetime.datetime = Field(description="Дата создания", alias="createdAt")


class ReportResponse(base_schema.BaseSchema):
    """
    Модель с данными об отчете
    """

    id: uuid.UUID = Field(description="Идентификатор отчета")
    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы", alias="magnetogramId")
    object_name: str = Field(description="Название объекта", alias="objectName")
    user_name: str = Field(description="Имя пользователя", alias="userName")
    created_at: datetime.datetime = Field(description="Дата создания", alias="createdAt")


class ReportObjectResponse(base_schema.BaseSchema):
    """
    Модель ответа с отчетом
    """

    report: bytes = Field(description="Отчет в формате байтовой строки")

    @field_validator("report", mode="after")
    @classmethod
    def convert_report_to_string(cls, report: bytes) -> str:
        """
        Конвертировать отчет из байтовой строки в обычную
        :param report: отчет в байтовой строке
        :return: отчет в обычной строке
        """

        return report.decode("utf-8")
