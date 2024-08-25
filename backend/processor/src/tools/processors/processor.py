import base64
import io
import pickle
import uuid

import cv2
import numpy as np

from dto import defect_dto, processor_dto, structural_unit_dto
from interfaces import base_processor
from tools import enums


class Processor(base_processor.AbstractProcessor):
    """
    Обрабтчик магнитограмм
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._magnetogram_pickle: bytes | None = None

    def _get_array_from_pickle(self) -> np.array:
        """
        Конвертировать магнитограмму в файле pickle в массив numpy
        :return: массив numpy
        """

        return pickle.load(io.BytesIO(self.magnetogram_pickle))

    def process(self) -> processor_dto.ProcessorDto:
        """
        Обработать магнитограмму
        :return: списки дефектов и структурных элементов
        """

        defects = [
            defect_dto.Defect(
                id=uuid.uuid4(),
                type_id=enums.Defect.ABSENCE.id,
                x_coord=0
            ),
            defect_dto.Defect(
                id=uuid.uuid4(),
                type_id=enums.Defect.PRESENCE.id,
                x_coord=1
            ),
            defect_dto.Defect(
                id=uuid.uuid4(),
                type_id=enums.Defect.PRESENCE.id,
                x_coord=2
            ),
            defect_dto.Defect(
                id=uuid.uuid4(),
                type_id=enums.Defect.ABSENCE.id,
                x_coord=3
            ),
            defect_dto.Defect(
                id=uuid.uuid4(),
                type_id=enums.Defect.ABSENCE.id,
                x_coord=4
            )
        ]

        structural_units = [
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.ABSENCE.id,
                x_coord=0
            ),
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.ABSENCE.id,
                x_coord=1
            ),
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.JOINT.id,
                x_coord=2
            ),
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.JOINT.id,
                x_coord=3
            ),
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.JOINT.id,
                x_coord=4
            ),
            structural_unit_dto.StructuralUnit(
                id=uuid.uuid4(),
                type_id=enums.StructuralUnit.JOINT.id,
                x_coord=5
            )
        ]

        return processor_dto.ProcessorDto(
            defects=defects,
            structural_units=structural_units
        )

    def get_processed_image(self) -> bytes:
        """
        Конвертировать массив из файла pickle в изображение
        :return: изображение в формате base64
        """

        image_array = self._get_array_from_pickle()
        success, image = cv2.imencode(".png", image_array)

        if not success:
            raise ValueError("Не удалось сгенерировать изображение")

        return base64.b64encode(image.tobytes())

    @property
    def magnetogram_pickle(self) -> bytes:
        """
        Свойство magnetogram_pickle
        :return: магнитограмма в формате pickle
        """

        return self._magnetogram_pickle

    @magnetogram_pickle.setter
    def magnetogram_pickle(self, value: bytes) -> None:
        """
        Установить значение для magnetogram_pickle
        :param value: значение для magnetogram_pickle
        """

        self._magnetogram_pickle = value
