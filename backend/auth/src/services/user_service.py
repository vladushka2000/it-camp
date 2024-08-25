import datetime
import uuid

from dependency_injector.wiring import Provide
from interfaces import base_schema, base_service
from pydantic import Field

from tools import consts, di_container, jwt_helper
from dto import user_dto


class UserService(base_service.AbstractService):
    """
    Сервис для работы с логикой действия над пользователями
    """

    class _DIFactoriesObjectsDTO(base_schema.PydanticBase):
        """
        DTO для объектов, получаемых из фабрик DI-контейнеров
        """

        jwt_helper_: jwt_helper.JWTHelper = Field(description="Утилита для работы с JWT")

    jwt_helper_factory = Provide[
        di_container.ToolsContainer.jwt_helper_factory
    ]

    @classmethod
    async def _get_di_objects(cls) -> _DIFactoriesObjectsDTO:
        """
        Получить объекты из фабрик DI-контейнеров
        """

        jwt_helper_ = cls.jwt_helper_factory.create()

        return cls._DIFactoriesObjectsDTO(
            jwt_helper_=jwt_helper_
        )

    @classmethod
    async def get_user_info_by_token(cls, access_token: str) -> user_dto.UserDTOBase:
        """
        Получить информацию о пользователе по его access-токену
        :param access_token: access-токен пользователя
        :return: информация о пользователе
        """

        di_objects = await cls._get_di_objects()
        jwt_manager = di_objects.jwt_helper_

        user_info = jwt_manager.get_payload_by_token(access_token, consts.Auth.ACCESS_TOKEN_ATTRS)

        return user_dto.UserDTOBase(
            id=uuid.UUID(user_info["sub"]),
            name=user_info["user_name"],
            role=uuid.UUID(user_info["role"]),
            created_at=datetime.datetime.fromtimestamp(user_info["created_at"])
        )
