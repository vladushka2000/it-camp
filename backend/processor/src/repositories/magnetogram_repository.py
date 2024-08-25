import uuid

from sqlalchemy import delete, exc, select

from dto import defect_dto, magnetogram_dto, structural_unit_dto
from interfaces import base_repository
from repositories.models import (
    defect_type_model,
    magnetogram_model,
    structural_unit_type_model
)
from tools import exceptions


class MagnetogramRepository(
    base_repository.AbstractAlchemyRepository,
    base_repository.CreateMixin,
    base_repository.RetrieveMixin,
    base_repository.UpdateMixin,
    base_repository.DeleteMixin
):
    """
    Репозиторий для работы с магнитограммами
    """

    def _create_defects(self, defects: list[defect_dto.Defect]) -> list[magnetogram_model.Defect]:
        """
        Создать список объектов дефектов
        :param defects: объекты дефектов
        :return: список объектов дефектов
        """

        return [
            magnetogram_model.Defect(
                id=defect.id,
                type_id=defect.type_id,
                x_coord=defect.x_coord,
                continue_for=defect.continue_for
            ) for defect in defects
        ]

    def _create_structural_units(
        self,
        structural_units: list[structural_unit_dto.StructuralUnit]
    ) -> list[magnetogram_model.StructuralUnit]:
        """
        Создать список объектов структурных элементов
        :param structural_units: объекты структурных элементов
        :return: список объектов структурных элементов
        """

        return [
            magnetogram_model.StructuralUnit(
                id=structural_unit.id,
                type_id=structural_unit.type_id,
                x_coord=structural_unit.x_coord,
                continue_for=structural_unit.continue_for
            ) for structural_unit in structural_units
        ]

    def _create_magnetogram(
        self,
        magnetogram: magnetogram_dto.MagnetogramProcessed,
        defect_db_models: list[magnetogram_model.Magnetogram] | None = None,
        structural_units_db_models: list[magnetogram_model.StructuralUnit] | None = None
    ) -> magnetogram_model.Magnetogram:
        """
        Создать объект магнитограммы
        :param magnetogram: объект магнитограммы
        :param defect_db_models: объекты дефектов
        :param structural_units_db_models: объекты структурных элементов
        """

        magnetogram_db_model = magnetogram_model.Magnetogram(
            id=magnetogram.id,
            object_name=magnetogram.object_name,
            user_name=magnetogram.user_name,
            comment=magnetogram.comment,
            magnetogram=magnetogram.magnetogram,
            created_at=magnetogram.created_at
        )

        if defect_db_models is not None:
            for defect in defect_db_models:
                magnetogram_db_model.defects.append(defect)

        if structural_units_db_models is not None:
            for structural_unit in structural_units_db_models:
                magnetogram_db_model.structural_units.append(structural_unit)

        return magnetogram_db_model

    async def create(
        self,
        magnetogram: magnetogram_dto.MagnetogramProcessed,
        defects: list[defect_dto.Defect],
        structural_units: list[structural_unit_dto.StructuralUnit]
    ) -> None:
        """
        Создать запись магнитограммы
        :param magnetogram: объект магнитограммы
        :param defects: объекты дефектов
        :param structural_units: объекты структурных элементов
        """

        defect_db_models = self._create_defects(defects)
        structural_unit_db_models = self._create_structural_units(structural_units)
        magnetogram_db_model = self._create_magnetogram(
            magnetogram,
            defect_db_models,
            structural_unit_db_models
        )

        self.session.add(magnetogram_db_model)

    async def retrieve(
        self,
        magnetogram_id: uuid.UUID | None = None
    ) -> magnetogram_model.Magnetogram | None:
        """
        Получить запись пользователя
        :param magnetogram_id: идентификатор магнитограммы
        :return: список отчетов
        """

        query = (
            select(magnetogram_model.Magnetogram).
            join(magnetogram_model.MagnetogramDefect, isouter=True).
            join(magnetogram_model.MagnetogramStructuralUnit, isouter=True).
            join(magnetogram_model.Defect, isouter=True).
            join(defect_type_model.DefectType, isouter=True).
            join(magnetogram_model.StructuralUnit, isouter=True).
            join(structural_unit_type_model.StructuralUnitType, isouter=True).
            where(magnetogram_model.Magnetogram.id == magnetogram_id)
        )

        result = await self.session.execute(query)

        try:
            return result.scalars().unique().one()
        except exc.NoResultFound:
            return

    async def retrieve_dto(
        self,
        magnetogram_id: uuid.UUID | None = None
    ) -> magnetogram_dto.MagnetogramWithElements | None:
        """
        Получить запись пользователя
        :param magnetogram_id: идентификатор магнитограммы
        :return: список отчетов
        """

        magnetogram = await self.retrieve(magnetogram_id)

        if not magnetogram:
            return

        defects = [
            defect_dto.Defect(
                id=defect.id,
                type_id=defect.type_id,
                x_coord=defect.x_coord,
                continue_for=defect.continue_for
            ) for defect in magnetogram.defects
        ]
        structural_units = [
            structural_unit_dto.StructuralUnit(
                id=structural_unit.id,
                type_id=structural_unit.type_id,
                x_coord=structural_unit.x_coord,
                continue_for=structural_unit.continue_for
            ) for structural_unit in magnetogram.structural_units
        ]

        magnetogram = magnetogram_dto.MagnetogramWithElements(
            id=magnetogram.id,
            user_name=magnetogram.user_name,
            object_name=magnetogram.object_name,
            magnetogram=magnetogram.magnetogram,
            comment=magnetogram.comment,
            created_at=magnetogram.created_at,
            structural_units=structural_units,
            defects=defects
        )

        return magnetogram

    async def update(
        self,
        magnetogram: magnetogram_model.Magnetogram,
        defects: list[defect_dto.Defect],
        structural_units: list[structural_unit_dto.StructuralUnit]
    ) -> None:
        """
        Создать запись магнитограммы
        :param magnetogram: объект магнитограммы
        :param defects: объекты дефектов
        :param structural_units: объекты структурных элементов
        """

        defect_db_models = self._create_defects(defects)
        structural_unit_db_models = self._create_structural_units(structural_units)

        for defect in defect_db_models:
            magnetogram.defects.append(defect)

        for structural_unit in structural_unit_db_models:
            magnetogram.structural_units.append(structural_unit)

        self.session.add_all(defect_db_models)
        self.session.add_all(structural_unit_db_models)

    async def delete(self, magnetogram_id: uuid.UUID) -> None:
        """
        Удалить запись магнитограммы и связанные с ней данные по дефектам и структурным элементам
        :param magnetogram_id: идентификатор магнитограммы
        """

        magnetogram_select_query = (
            select(magnetogram_model.Magnetogram).
            where(magnetogram_model.Magnetogram.id == magnetogram_id)
        )

        magnetogram = await self.session.execute(magnetogram_select_query)
        magnetogram = magnetogram.scalars().unique().one()

        if not magnetogram:
            raise exceptions.UserFaultException("Магнитограмма не была найдена")

        defect_ids = [defect.id for defect in magnetogram.defects]
        structural_units_ids = [structural_unit.id for structural_unit in magnetogram.structural_units]

        magnetogram.defects.clear()
        magnetogram.structural_units.clear()

        await self.session.execute(
            magnetogram_model.Defect.__table__.delete().where(magnetogram_model.Defect.id.in_(defect_ids))
        )

        await self.session.execute(
            magnetogram_model.StructuralUnit.__table__.delete().
            where(magnetogram_model.StructuralUnit.id.in_(structural_units_ids))
        )
