from interfaces import base_factory
from uow import alchemy_uow, alchemy_redis_uow_composite, redis_uow


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


class RedisUOWFactory(base_factory.AbstractFactory):
    """
    Фабрика UOW для работы с репозиториями Redis
    """

    def create(self) -> redis_uow.RedisUOW:
        """
        Создать объект UOW
        :return: объект UOW
        """

        return redis_uow.RedisUOW()


class AlchemyRedisUOWCompositeFactory(base_factory.AbstractFactory):
    """
    Фабрика компоновщика UOW для работы с репозиториями Алхимии и Redis
    """

    def create(self) -> alchemy_redis_uow_composite.AlchemyRedisUOWComposite:
        """
        Создать объект компоновщика UOW
        :return: объект UOW
        """

        return alchemy_redis_uow_composite.AlchemyRedisUOWComposite()
