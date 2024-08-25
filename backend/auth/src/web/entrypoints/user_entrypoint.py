from fastapi import APIRouter, Depends

from services import user_service
from web.schemas import user_schema
from web.dependencies import token_dependency

router = APIRouter(prefix="/users")


@router.get("/token-info")
async def get_token_info(
    token: str = Depends(token_dependency.get_access_token),
) -> user_schema.UserInfoModel:
    """
    Получить информацию о пользователе по его access-токену
    :param token: access-токен
    :return: информация о пользователе
    """

    result = await user_service.UserService.get_user_info_by_token(token)

    return user_schema.UserInfoModel(
        id=result.id,
        name=result.name,
        role_id=result.role,
        created_at=result.created_at
    )
