from dependency_injector import containers, providers

from config import app_config
from tools.factories import repository_factory, session_factory, uow_factory

config = app_config.config


class SessionContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами сессий
    """

    alchemy_session_factory = providers.Factory(session_factory.AlchemySessionFactory)


class RepositoryContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами репозиториев
    """

    report_repository_factory = providers.Factory(
        repository_factory.ReportRepositoryFactory
    )


class UOWContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами UOW
    """

    alchemy_uow_factory = providers.Factory(uow_factory.AlchemyUOWFactory)
