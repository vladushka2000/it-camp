from fastapi import status, FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from config import app_config
from tools import di_container, exceptions
from web.tools import router_registrator

config = app_config.config

app = FastAPI(
    debug=config.is_dev,
    title=config.app_name,
    version=config.app_version
)


@app.exception_handler(Exception)
async def universal_exception_handler(_, exception: Exception) -> JSONResponse:
    """
    Обработать ошибку
    :param exception: объект ошибки
    :return: ответ сервера с описанием ошибки
    """

    if isinstance(exception, exceptions.UserFaultException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Произошла ошибка из-за неверного ввода"},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Произошла ошибка на стороне сервера"},
    )


router_registrator.register_routers(app)


if __name__ == "__main__":
    session_container = di_container.SessionContainer()
    repository_container = di_container.RepositoryContainer()
    uow_container = di_container.UOWContainer()
    tools_container = di_container.ToolsContainer()

    service_modules = [
        "services.processor_service",
        "services.history_service"
    ]

    session_container.wire(modules=service_modules)
    repository_container.wire(modules=service_modules)
    uow_container.wire(modules=service_modules)
    tools_container.wire(modules=service_modules)

    uvicorn.run(app, host=config.app_host, port=config.app_port)
