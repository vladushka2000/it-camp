import datetime
import uuid

from pydantic import Field

from interfaces import base_schema


class ReportDataDTO(base_schema.BaseSchema):
    """
    DTO, содержащий информацию об отчете
    """

    id: uuid.UUID = Field(description="Идентификатор отчета")
    magnetogram_id: uuid.UUID = Field(description="Идентификатор магнитограммы")
    user_name: str = Field(description="Имя пользователя")
    report: bytes = Field(description="Отчет в формате байтовой строки")
    created_at: datetime.datetime = Field(description="Дата создания", default=datetime.datetime.now())


class ReportDataMagnetogramInfoDTO(ReportDataDTO):
    """
    DTO, содержащий информацию об отчете и магнитограмме
    """

    object_name: str = Field(description="Название объекта")
