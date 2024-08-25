from fastapi import status, APIRouter, Depends, HTTPException

from dto import auth_dto
from services import auth_service
from web.dependencies import token_dependency
from web.schemas import auth_schema

router = APIRouter(prefix="/auth")


@router.post("/sign-up")
async def sign_up(
    user: auth_schema.AuthModel,
) -> auth_schema.JWTModel:
    """
    Зарегистрироваться в приложении
    :param user: данные пользователя
    :return: токены
    """

    user_creds = auth_dto.AuthDTO(name=user.name, password=user.password)

    result = await auth_service.AuthService.sign_up_user(user_creds)

    if result.status == status.HTTP_201_CREATED:
        return auth_schema.JWTModel(
            access_token=result.payload["accessToken"], refresh_token=result.payload["refreshToken"]
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.post("/sign-in")
async def sign_in(user: auth_schema.AuthModel) -> auth_schema.JWTModel:
    """
    Войти в приложение по логину и паролю
    :param user: данные пользователя
    :return: токены
    """

    user_creds = auth_dto.AuthDTO(name=user.name, password=user.password)

    result = await auth_service.AuthService.sign_in_user(user_creds)

    if result.status == status.HTTP_200_OK:
        return auth_schema.JWTModel(
            access_token=result.payload["accessToken"], refresh_token=result.payload["refreshToken"]
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )


@router.get("/refresh-tokens")
async def refresh_tokens(
    token: str = Depends(token_dependency.get_token),
) -> auth_schema.JWTModel:
    """
    Обновить access и refresh-токены
    :param token: refresh-токен
    :return: обновленные access и refresh-токены
    """

    result = await auth_service.AuthService.refresh_tokens(token)

    if result.status == status.HTTP_200_OK:
        return auth_schema.JWTModel(
            access_token=result.payload["accessToken"], refresh_token=result.payload["refreshToken"]
        )

    raise HTTPException(
        status_code=result.status,
        detail=result.payload["detail"]
    )
