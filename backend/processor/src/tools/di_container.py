from dependency_injector import containers, providers

from config import app_config
from tools.factories import repository_factory, session_factory, tools_factory, uow_factory

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

    magnetogram_repository_factory = providers.Factory(
        repository_factory.MagnetogramRepositoryFactory
    )
    history_repository_factory = providers.Factory(
        repository_factory.HistoryRepositoryFactory
    )


class UOWContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами UOW
    """

    alchemy_uow_factory = providers.Factory(uow_factory.AlchemyUOWFactory)


class ToolsContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами утилит
    """

    processor_factory = providers.Factory(tools_factory.ProcessorFactory)
    truncator_factory = providers.Factory(tools_factory.TruncatorFactory)
