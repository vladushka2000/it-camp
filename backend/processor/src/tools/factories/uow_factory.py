from interfaces import base_factory
from uow import alchemy_uow


class AlchemyUOWFactory(base_factory.AbstractFactory):
    """
    Фабрика UOW для работы с репозиториями Алхимии
    """

    def create(self) -> alchemy_uow.AlchemyUOW:
        """
        Создать объект UOW
        :return: объект UOW
        """

        return alchemy_uow.AlchemyUOW()
