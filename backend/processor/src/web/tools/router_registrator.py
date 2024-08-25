from fastapi import FastAPI

from web.entrypoints import history_entrypoint, processor_entrypoint


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(history_entrypoint.router)
    app.include_router(processor_entrypoint.router)
