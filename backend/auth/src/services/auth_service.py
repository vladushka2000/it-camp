import datetime
import uuid

from dependency_injector.wiring import Provide
from pydantic import Field
from redis.asyncio.client import Pipeline
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import base_repository, base_service, base_uow, base_schema
from tools import consts, di_container, enums, exceptions, jwt_helper, password_helper
from dto import auth_dto, user_dto


class AuthService(base_service.AbstractService):
    """
    Сервис для работы с логикой авторизации и аутентификации
    """

    class _DIFactoriesObjectsDTO(base_schema.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        alchemy_session: AsyncSession = Field(description="Сессия Алхимии")
        redis_session: Pipeline = Field(description="Сессия Redis")

        user_repository: base_repository.AbstractAlchemyRepository = Field(
            description="Репозиторий для работы с пользователями"
        )
        token_repository: base_repository.AbstractRedisRepository = Field(
            description="Репозиторий для работы с токенами"
        )

        alchemy_uow: base_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Алхимии"
        )
        redis_uow: base_uow.AbstractUOW = Field(
            description="UOW для работы с репозиториями Redis"
        )

    alchemy_session_factory = Provide[
        di_container.SessionContainer.alchemy_session_factory
    ]
    redis_token_session_factory = Provide[
        di_container.SessionContainer.redis_token_session_factory
    ]

    user_repository_factory = Provide[
        di_container.RepositoryContainer.user_repository_factory
    ]
    token_repository_factory = Provide[
        di_container.RepositoryContainer.token_repository_factory
    ]

    alchemy_uow_factory = Provide[di_container.UOWContainer.alchemy_uow_factory]
    redis_uow_factory = Provide[di_container.UOWContainer.redis_uow_factory]

    @classmethod
    async def _get_di_objects(cls) -> _DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        async with cls.alchemy_session_factory.session_maker() as async_session:
            alchemy_session = async_session

        redis_session = cls.redis_token_session_factory.create()

        user_repository = cls.user_repository_factory.create(alchemy_session)
        token_repository = cls.token_repository_factory.create(redis_session)

        alchemy_uow = cls.alchemy_uow_factory.create()
        alchemy_uow.add_repository(user_repository.name, user_repository)

        redis_uow = cls.redis_uow_factory.create()
        redis_uow.add_repository(token_repository.name, token_repository)

        return cls._DIFactoriesObjectsDTO(
            alchemy_session=alchemy_session,
            redis_session=redis_session,
            user_repository=user_repository,
            token_repository=token_repository,
            alchemy_uow=alchemy_uow,
            redis_uow=redis_uow,
        )

    @classmethod
    async def sign_up_user(cls, user_model: auth_dto.AuthDTO) -> auth_dto.TokensDTO:
        """
        Выполнить логику регистрации пользователя
        :param user_model: данные пользователя
        :return: токены
        """

        di_objects = await cls._get_di_objects()
        password_manager = password_helper.PasswordHelper(
            enums.PasswordHasherAlgorithm.BCRYPT
        )
        jwt_manager = jwt_helper.JWTHelper()

        user = user_dto.UserDTO(
            id=uuid.uuid4(),
            name=user_model.name,
            password=password_manager.encode_password(user_model.password),
            created_at=datetime.datetime.now(),
            role=enums.Role.EXPERT.id
        )

        async with di_objects.alchemy_uow:
            if await di_objects.alchemy_uow.repositories[
                di_objects.user_repository.name
            ].retrieve(user_name=user_model.name):
                raise exceptions.UserFaultException("Пользователь уже зарегистрирован")

            di_objects.alchemy_uow.repositories[di_objects.user_repository.name].create(
                user
            )

            await di_objects.alchemy_uow.commit()

        access_token = jwt_manager.issue_jwt(user, consts.Auth.ACCESS_TOKEN_ATTRS)
        refresh_token = jwt_manager.issue_jwt(user, consts.Auth.REFRESH_TOKEN_ATTRS)

        user_refresh_token_dto = auth_dto.UsersRefreshToken(
            user_id=user.id, refresh_token=refresh_token
        )

        async with di_objects.redis_uow:
            await di_objects.redis_uow.repositories[
                di_objects.token_repository.name
            ].create(
                user_refresh_token_dto,
                consts.Auth.REFRESH_TOKEN_ATTRS.expiration_time_in_sec,
            )

            await di_objects.redis_uow.commit()

        return auth_dto.TokensDTO(
            access_token=access_token, refresh_token=refresh_token
        )

    @classmethod
    async def sign_in_user(cls, user_model: auth_dto.AuthDTO) -> auth_dto.TokensDTO:
        """
        Выполнить логику входа пользователя в приложение
        :param user_model: данные пользователя
        :return: токены
        """

        di_objects = await cls._get_di_objects()
        password_manager = password_helper.PasswordHelper(
            enums.PasswordHasherAlgorithm.BCRYPT
        )
        jwt_manager = jwt_helper.JWTHelper()

        async with di_objects.alchemy_uow:
            user = await di_objects.alchemy_uow.repositories[
                di_objects.user_repository.name
            ].retrieve(user_name=user_model.name)

            if user is None:
                raise exceptions.UserFaultException("Пользователь не зарегистрирован")

            if not password_manager.is_password_valid(
                user_model.password, user.password
            ):
                raise exceptions.UserFaultException("Неверный пароль")

        access_token = jwt_manager.issue_jwt(user, consts.Auth.ACCESS_TOKEN_ATTRS)
        refresh_token = jwt_manager.issue_jwt(user, consts.Auth.REFRESH_TOKEN_ATTRS)

        user_refresh_token_dto = auth_dto.UsersRefreshToken(
            user_id=user.id, refresh_token=refresh_token
        )

        async with di_objects.redis_uow:
            await di_objects.redis_uow.repositories[
                di_objects.token_repository.name
            ].create(
                user_refresh_token_dto,
                consts.Auth.REFRESH_TOKEN_ATTRS.expiration_time_in_sec,
            )

            await di_objects.redis_uow.commit()

        return auth_dto.TokensDTO(
            access_token=access_token, refresh_token=refresh_token
        )

    @classmethod
    async def refresh_tokens(cls, refresh_token: str) -> auth_dto.TokensDTO:
        """
        Выполнить логику обновления токенов пользователя
        :param refresh_token: refresh-токен пользователя
        :return: обновленные токены
        """

        di_objects = await cls._get_di_objects()
        jwt_manager = jwt_helper.JWTHelper()

        refresh_payload = jwt_manager.get_payload_by_token(
            refresh_token, consts.Auth.REFRESH_TOKEN_ATTRS
        )

        async with di_objects.alchemy_uow:
            user = await di_objects.alchemy_uow.repositories[
                di_objects.user_repository.name
            ].retrieve(user_id=refresh_payload["sub"])

            if user is None:
                raise exceptions.UserFaultException("Пользователь не найден")

        new_access_token = jwt_manager.issue_jwt(user, consts.Auth.ACCESS_TOKEN_ATTRS)
        new_refresh_token = jwt_manager.issue_jwt(user, consts.Auth.REFRESH_TOKEN_ATTRS)

        user_refresh_token_dto = auth_dto.UsersRefreshToken(
            user_id=user.id, refresh_token=refresh_token
        )

        async with di_objects.redis_uow:
            await di_objects.redis_uow.repositories[
                di_objects.token_repository.name
            ].retrieve(user_refresh_token_dto.user_id)

            current_refresh_token = (await di_objects.redis_uow.commit())[0]

            if current_refresh_token is None:
                raise exceptions.UserFaultException("Токен не был найден в базе данных")

            current_refresh_token = current_refresh_token.decode("utf-8")

            if current_refresh_token != refresh_token:
                await di_objects.redis_uow.repositories[
                    di_objects.token_repository.name
                ].delete(user_refresh_token_dto.user_id)

                await di_objects.redis_uow.commit()

                raise exceptions.UserFaultException("Refresh-токены не совпадают")

            await di_objects.redis_uow.repositories[
                di_objects.token_repository.name
            ].create(
                user_refresh_token_dto,
                consts.Auth.REFRESH_TOKEN_ATTRS.expiration_time_in_sec,
            )

            await di_objects.redis_uow.commit()

        return auth_dto.TokensDTO(
            access_token=new_access_token, refresh_token=new_refresh_token
        )
