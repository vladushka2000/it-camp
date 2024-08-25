from fastapi import FastAPI

from web.entrypoints import (
    auth_entrypoint,
    processor_entrypoint,
    reporter_entrypoint
)


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(auth_entrypoint.router)
    app.include_router(processor_entrypoint.router)
    app.include_router(reporter_entrypoint.router)
