import datetime
import uuid

from fastapi import status, APIRouter

from dto import defect_dto, magnetogram_dto, structural_unit_dto
from services import processor_service
from web.schemas import magnetogram_schema

router = APIRouter(prefix="/processor")


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_magnetogram(
    magnetogram: magnetogram_schema.MagnetogramRequest,
) -> magnetogram_schema.MagnetogramResponse:
    """
    Загрузить магнитограмму
    :param magnetogram: данные о магнитограмме
    :return: обработанная магнитограмма
    """

    magnetogram_info = magnetogram_dto.MagnetogramToProcess(
        id=uuid.uuid4(),
        user_name=magnetogram.user_name,
        object_name=magnetogram.object_name,
        magnetogram=magnetogram.magnetogram,
        comment=magnetogram.comment,
        created_at=datetime.datetime.now()
    )

    processed_magnetogram = await processor_service.ProcessorService.upload_magnetogram(magnetogram_info)

    return magnetogram_schema.MagnetogramResponse(
        user_name=processed_magnetogram.user_name,
        object_name=processed_magnetogram.object_name,
        magnetogram=processed_magnetogram.magnetogram,
        comment=processed_magnetogram.comment,
        magnetogram_id=processed_magnetogram.id,
        structural_units=[
            magnetogram_schema.StructuralUnitResponse(
                id=structural_unit.id,
                type_id=structural_unit.type_id,
                type_name=structural_unit.type_name,
                x_coord=structural_unit.x_coord,
                continue_for=structural_unit.continue_for
            ) for structural_unit in processed_magnetogram.structural_units
        ],
        defects=[
            magnetogram_schema.DefectResponse(
                id=defect.id,
                type_id=defect.type_id,
                type_name=defect.type_name,
                x_coord=defect.x_coord,
                continue_for=defect.continue_for
            ) for defect in processed_magnetogram.defects
        ],
        created_at=processed_magnetogram.created_at
    )


@router.get("/magnetograms/{magnetogram_id}")
async def get_magnetogram(
    magnetogram_id: uuid.UUID,
) -> magnetogram_schema.MagnetogramResponse:
    """
    Получить магнитограмму
    :param magnetogram_id: идентификатор магнитограммы
    :return: данные обработанной магнитограммы
    """

    magnetogram = await processor_service.ProcessorService.get_magnetogram(magnetogram_id)

    return magnetogram_schema.MagnetogramResponse(
        magnetogram_id=magnetogram.id,
        object_name=magnetogram.object_name,
        user_name=magnetogram.user_name,
        magnetogram=magnetogram.magnetogram,
        comment=magnetogram.comment,
        structural_units=[
            magnetogram_schema.StructuralUnitResponse(
                id=structural_unit.id,
                type_id=structural_unit.type_id,
                type_name=structural_unit.type_name,
                x_coord=structural_unit.x_coord,
                continue_for=structural_unit.continue_for
            ) for structural_unit in magnetogram.structural_units
        ],
        defects=[
            magnetogram_schema.DefectResponse(
                id=defect.id,
                type_id=defect.type_id,
                type_name=defect.type_name,
                x_coord=defect.x_coord,
                continue_for=defect.continue_for
            ) for defect in magnetogram.defects
        ],
        created_at=magnetogram.created_at
    )


@router.patch("/magnetograms/{magnetogram_id}/edit", status_code=status.HTTP_201_CREATED)
async def edit_magnetogram(
    magnetogram_id: uuid.UUID,
    edit_data: magnetogram_schema.MagnetogramEditRequest
) -> None:
    """
    Редактировать магнитограмму
    :param magnetogram_id: идентификатор магнитограммы
    :param edit_data: данные для обновления
    """

    new_defects_model = [
        defect_dto.Defect(
            id=uuid.uuid4(),
            type_id=defect.type_id,
            x_coord=defect.x_coord
        ) for defect in edit_data.new_defects
    ]
    new_structural_units_model = [
        structural_unit_dto.StructuralUnit(
            id=uuid.uuid4(),
            type_id=structural_unit.type_id,
            x_coord=structural_unit.x_coord
        ) for structural_unit in edit_data.new_structural_units
    ]

    await processor_service.ProcessorService.edit_magnetogram(
        magnetogram_id,
        new_defects_model,
        new_structural_units_model
    )
