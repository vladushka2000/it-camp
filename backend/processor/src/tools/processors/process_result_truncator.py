from dto import defect_dto, structural_unit_dto
from interfaces import base_util
from tools import enums


class ProcessResultTrancutor(base_util.AbstractUtil):
    """
    Форматтер результата обработчика
    """

    def truncate_process_result(
        self,
        elements: list[defect_dto.Defect | structural_unit_dto.StructuralUnit]
    ) -> list[defect_dto.Defect | structural_unit_dto.StructuralUnit]:
        """
        Отформатировать результат обработчика
        :param elements: список дефектов или структурных элементов
        :return: отформатированный результат обработчика
        """

        def _check_for_absence(element: defect_dto.Defect | structural_unit_dto.StructuralUnit) -> bool:
            """
            Проверить элемент на тип Отсутствие
            :param element: элемент
            :return: True, если элемент принадлежит типу Отсутствие, иначе - False
            """

            return element.type_id in (
                enums.Defect.ABSENCE.id, enums.StructuralUnit.ABSENCE.id
            )

        formatted = []

        if not elements:
            return []

        current_index = 0

        while current_index < len(elements):
            current_element = elements[current_index]
            current_index += 1

            if _check_for_absence(current_element):
                continue

            for cursor in range(current_index, len(elements)):
                if current_element.type_id == elements[cursor].type_id and not _check_for_absence(elements[cursor]):
                    current_element.continue_for += 1
                    current_index += 1
                else:
                    break

            formatted.append(current_element)

        return formatted
