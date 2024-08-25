from dependency_injector import containers, providers

from tools.factories import connection_factory, repository_factory


class SessionContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами сессий
    """

    http_session_factory = providers.Singleton(connection_factory.HTTPSessionFactory)


class RepositoryContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами репозиториев
    """

    http_repository_factory = providers.Factory(
        repository_factory.HTTPRepositoryFactory
    )
