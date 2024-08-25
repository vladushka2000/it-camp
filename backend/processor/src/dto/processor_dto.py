from pydantic import Field

from dto import defect_dto, structural_unit_dto
from interfaces import base_schema


class ProcessorDto(base_schema.BaseSchema):
    """
    Модель выходных данных, получаемых из обработчика магнитограммы
    """

    defects: list[defect_dto.Defect] = Field(description="Список дефектов")
    structural_units: list[structural_unit_dto.StructuralUnit] = Field(description="Список структурных элементов")
