from __future__ import annotations  # no qa

import abc

from interfaces import base_repository


class AbstractUOW(abc.ABC):
    """
    Абстрактный класс UOW
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.repositories: dict[str, base_repository.AbstractRepository] = {}

    def add_repository(
        self, repository_name: str, repository: base_repository.AbstractRepository
    ) -> None:
        """
        Добавить репозиторий
        :param repository_name: название репозитория
        :param repository: объект репозитория
        """

        self.repositories[repository_name] = repository

    async def __aenter__(self, *args, **kwargs) -> AbstractUOW:
        """
        Войти в асинхронный контекстный менеджер
        """

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из асинхронного контекстного менеджера
        """

        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        raise NotImplementedError
