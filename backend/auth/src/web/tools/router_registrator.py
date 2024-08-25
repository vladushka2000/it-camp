from fastapi import FastAPI

from web.entrypoints import (
    auth_entrypoint,
    user_entrypoint
)


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(auth_entrypoint.router)
    app.include_router(user_entrypoint.router)
