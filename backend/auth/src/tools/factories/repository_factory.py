from redis.asyncio.client import Pipeline
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_factory
from repositories import (
    token_repository,
    user_repository,
)
from tools import enums


class UserRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с пользователями
    """

    def create(self, session: AsyncSession) -> user_repository.UserRepository:
        """
        Создать объект репозитория
        :param session: сессия Алхимии
        :return: объект репозитория
        """

        return user_repository.UserRepository(
            enums.RepositoryName.USER_REPOSITORY.value, session
        )


class TokenRepositoryFactory(base_factory.AbstractFactory):
    """
    Фабрика репозиториев для работы с репозиторием токенов
    """

    def create(self, session: Pipeline) -> token_repository.TokenRepository:
        """
        Создать объект репозитория
        :param session: сессия Redis
        :return: объект репозитория
        """

        return token_repository.TokenRepository(
            enums.RepositoryName.TOKEN_REPOSITORY.value, session
        )
