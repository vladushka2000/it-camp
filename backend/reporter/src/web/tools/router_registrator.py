from fastapi import FastAPI

from web.entrypoints import (
    report_entrypoint
)


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(report_entrypoint.router)
