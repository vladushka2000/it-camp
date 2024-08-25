import uuid

from fastapi import status, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dto import user_dto
from services import user_service
from tools import enums

__http_bearer = HTTPBearer()


def get_token(
    creds: HTTPAuthorizationCredentials = Depends(__http_bearer),
) -> str:
    """
    Получить токен
    :param creds: данные авторизации
    :return: токен
    """

    return creds.credentials


async def get_user_info(token: str = Depends(get_token)) -> user_dto.UserDataDTO:
    """
    Получить информацию о пользователе по его токену
    :param token: токен пользователя
    :return: информация о пользователе
    """

    result = await user_service.UserService.get_user_info_by_token(token)

    if result.status == status.HTTP_200_OK:
        return user_dto.UserDataDTO(
            user_id=result.payload["id"],
            user_name=result.payload["name"],
            role_id=result.payload["roleId"],
            created_at=result.payload["createdAt"]
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


class RoleChecker:
    """
    Класс, вызов которого проверяет роль пользователя на соответствие переданной роли
    """

    def __init__(self, required_role: enums.Role) -> None:
        """
        Инициализировать переменные
        :param required_role: требуемая роль пользователя
        """

        self.required_role = required_role

    async def __call__(self, user_info: user_dto.UserDataDTO = Depends(get_user_info)) -> uuid.UUID:
        """
        Сверить переданную роль пользователя с требуемой ролью
        :param user_info: информация о пользователе
        :return: роль пользователя
        """

        actual_role = user_info.role_id

        if self.required_role.id != actual_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для доступа к ресурсу"
            )

        return actual_role
