import base64
import datetime
import uuid

from pydantic import field_validator, Field

from interfaces import base_schema
from tools import consts


class ReportDataDTO(base_schema.BaseSchema):
    """
    DTO, содержащий информацию об отчете
    """

    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы")
    report: bytes = Field(description="Отчет в формате байтовой строки")
    user_name: str = Field(description="Имя пользователя")
    created_at: datetime.datetime = Field(description="Дата создания")

    @field_validator("magnetogram_id", mode="after")
    @classmethod
    def convert_magnetogram_id_to_str(cls, value: uuid.UUID) -> str:
        """
        Конвертировать идентификатор магнитограммы из UUID в строку
        :param value: идентификатор магнитограммы в формате UUID
        :return: идентификатор магнитограммы в формате строки
        """

        return str(value)

    @field_validator("report", mode="after")
    @classmethod
    def convert_report_to_str(cls, report: bytes) -> str:
        """
        Конвертировать отчет из байтовой строки в обычную строку
        :param report: отчет в байтовой строке
        :return: отчет в обычной строке
        """

        return report.decode("utf-8")

    @field_validator("created_at", mode="after")
    @classmethod
    def convert_date_to_str(cls, value: datetime.datetime) -> str:
        """
        Конвертировать время в строку
        :param value: объект времени
        :return: строка времени
        """

        return value.strftime(consts.Time.STR_TIME_FORMAT)
