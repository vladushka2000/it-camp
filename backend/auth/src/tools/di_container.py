from dependency_injector import containers, providers

from config import app_config
from tools.factories import repository_factory, session_factory, tools_factory, uow_factory

config = app_config.config


class SessionContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами сессий
    """

    alchemy_session_factory = providers.Factory(session_factory.AlchemySessionFactory)
    redis_token_session_factory = providers.Factory(
        session_factory.RedisTokenSessionFactory, config.redis_token_dsn
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами репозиториев
    """

    user_repository_factory = providers.Factory(
        repository_factory.UserRepositoryFactory
    )
    token_repository_factory = providers.Factory(
        repository_factory.TokenRepositoryFactory
    )


class UOWContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами UOW
    """

    alchemy_uow_factory = providers.Factory(uow_factory.AlchemyUOWFactory)
    redis_uow_factory = providers.Factory(uow_factory.RedisUOWFactory)
    alchemy_redis_uow_composite_factory = providers.Factory(
        uow_factory.AlchemyRedisUOWCompositeFactory
    )


class ToolsContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами утилит
    """

    jwt_helper_factory = providers.Factory(tools_factory.JWTHelperFactory)
