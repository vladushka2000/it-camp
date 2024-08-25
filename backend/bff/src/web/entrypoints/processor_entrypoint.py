import datetime
import uuid

from fastapi import status, APIRouter, Depends, HTTPException, Query

from dto import processor_dto
from services import processor_service
from tools import enums
from web.dependencies import token_dependency
from web.schemas import processor_schema

router = APIRouter(prefix="/processor")


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_magnetogram(
    magnetogram: processor_schema.MagnetogramRequest,
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> processor_schema.MagnetogramResponse:
    """
    Загрузить магнитограмму
    :param magnetogram: данные о магнитограмме
    :param role: роль пользователя
    :return: обработанная магнитограмма
    """

    magnetogram_info = processor_dto.MagnetogramToUpload(
        user_name=magnetogram.user_name,
        object_name=magnetogram.object_name,
        magnetogram=magnetogram.magnetogram,
        comment=magnetogram.comment
    )

    result = await processor_service.ProcessorService.upload_magnetogram(magnetogram_info)

    if result.status == status.HTTP_201_CREATED:
        payload = result.payload

        return processor_schema.MagnetogramResponse(
            magnetogram_id=payload["magnetogramId"],
            magnetogram=payload["magnetogram"],
            structural_units=[
                processor_schema.StructuralUnitResponse(
                    id=structural_unit["id"],
                    type_id=structural_unit["typeId"],
                    type_name=structural_unit["typeName"],
                    x_coord=structural_unit["xCoord"],
                    continue_for=structural_unit["continueFor"]
                ) for structural_unit in payload["structuralUnits"]
            ],
            defects=[
                processor_schema.DefectResponse(
                    id=defect["id"],
                    type_id=defect["typeId"],
                    type_name=defect["typeName"],
                    x_coord=defect["xCoord"],
                    continue_for=defect["continueFor"]
                ) for defect in payload["defects"]
            ],
            created_at=payload["createdAt"],
            object_name=payload["objectName"],
            comment=payload["comment"],
            user_name=payload['userName']
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.get("/magnetograms/{magnetogram_id}")
async def get_magnetogram(
    magnetogram_id: uuid.UUID,
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> processor_schema.MagnetogramResponse:
    """
    Получить магнитограмму
    :param magnetogram_id: идентификатор магнитограммы
    :param role: роль пользователя
    :return: обработанная магнитограмма
    """

    result = await processor_service.ProcessorService.get_magnetogram(magnetogram_id)

    if result.status == status.HTTP_200_OK:
        payload = result.payload

        return processor_schema.MagnetogramResponse(
            magnetogram_id=payload["magnetogramId"],
            magnetogram=payload["magnetogram"],
            structural_units=[
                processor_schema.StructuralUnitResponse(
                    id=structural_unit["id"],
                    type_id=structural_unit["typeId"],
                    type_name=structural_unit["typeName"],
                    x_coord=structural_unit["xCoord"],
                    continue_for=structural_unit["continueFor"]
                ) for structural_unit in payload["structuralUnits"]
            ],
            defects=[
                processor_schema.DefectResponse(
                    id=defect["id"],
                    type_id=defect["typeId"],
                    type_name=defect["typeName"],
                    x_coord=defect["xCoord"],
                    continue_for=defect["continueFor"]
                ) for defect in payload["defects"]
            ],
            created_at=payload["createdAt"],
            object_name=payload["objectName"],
            comment=payload["comment"],
            user_name=payload['userName']
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.patch("/magnetograms/{magnetogram_id}/edit", status_code=status.HTTP_201_CREATED)
async def edit_magnetogram(
    magnetogram_id: uuid.UUID,
    edit_data: processor_schema.MagnetogramEditRequest,
    role=Depends(token_dependency.RoleChecker(enums.Role.EXPERT))  # no qa
) -> None:
    """
    Редактировать магнитограмму
    :param magnetogram_id: идентификатор магнитограммы
    :param edit_data: данные для обновления
    :param role: роль пользователя
    """

    new_defects_model = [
        processor_dto.Defect(
            id=uuid.uuid4(),
            type_id=defect.type_id,
            x_coord=defect.x_coord
        ) for defect in edit_data.new_defects
    ]
    new_structural_units_model = [
        processor_dto.StructuralUnit(
            id=uuid.uuid4(),
            type_id=structural_unit.type_id,
            x_coord=structural_unit.x_coord
        ) for structural_unit in edit_data.new_structural_units
    ]

    data = processor_dto.MagnetogramEdit(
        new_defects=new_defects_model,
        new_structural_units=new_structural_units_model
    )

    result = await processor_service.ProcessorService.edit_magnetogram(magnetogram_id, data)

    if result.status != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=result.status,
            detail=result.payload["detail"] if result.payload else None
        )


@router.get("/history")
async def get_history(
    date_from: datetime.datetime = Query(alias="dateFrom"),
    date_to: datetime.datetime = Query(alias="dateTo")
) -> list[processor_schema.History]:
    """
    Получить отчеты
    :param date_from: дата начала просмотра
    :param date_to: дата конца просмотра
    :return: список записей истории
    """

    result = await processor_service.ProcessorService.get_history(date_from, date_to)

    if result.status == status.HTTP_200_OK:
        return [
            processor_schema.History(
                id=record["id"],
                magnetogram_id=record["magnetogramId"],
                action_type_id=record["actionTypeId"],
                type_name=record["typeName"],
                user_name=record["userName"],
                date=record["date"]
            )
            for record in result.payload
        ]

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )
