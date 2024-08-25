import uuid

from interfaces import base_enum, base_util


class EnumUtil(base_util.AbstractUtil):
    """
    Класс для работы с Enum
    """

    @staticmethod
    def get_value_by_id(id_: uuid.UUID, enum_: type(base_enum.AbstractIdNameEnum)) -> any:
        """
        Получить значение по переданному идентификатору в Enum, состоящем из идентификатора и значения
        :param id_: идентификатор
        :param enum_: Enum, в котором производится поиск
        :return: значение, полученное по идентификатору
        """

        for key in enum_:
            if key.id == id_:
                return key.value

        raise ValueError("Элемент не был найден")
