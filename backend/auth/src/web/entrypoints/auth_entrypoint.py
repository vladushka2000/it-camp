from fastapi import status, APIRouter, Depends

from dto import auth_dto
from services import auth_service
from web.schemas import auth_schema
from web.dependencies import token_dependency

router = APIRouter(prefix="/auth")


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(
    user: auth_schema.AuthModel,
) -> auth_schema.JWTModel:
    """
    Зарегистрироваться в приложении
    :param user: данные пользователя
    :return: токены
    """

    user_dto = auth_dto.AuthDTO(name=user.name, password=user.password)

    tokens = await auth_service.AuthService.sign_up_user(user_dto)

    return auth_schema.JWTModel(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.post("/sign-in")
async def sign_in(user: auth_schema.AuthModel) -> auth_schema.JWTModel:
    """
    Войти в приложение по логину и паролю
    :param user: данные пользователя
    :return: токены
    """

    user_dto = auth_dto.AuthDTO(name=user.name, password=user.password)

    tokens = await auth_service.AuthService.sign_in_user(user_dto)

    return auth_schema.JWTModel(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.get("/refresh-tokens")
async def refresh_tokens(
    token: str = Depends(token_dependency.get_refresh_token),
) -> auth_schema.JWTModel:
    """
    Обновить access и refresh-токены
    :param token: refresh-токен
    :return: обновленные access и refresh-токены
    """

    tokens = await auth_service.AuthService.refresh_tokens(token)

    return auth_schema.JWTModel(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )
