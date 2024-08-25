import contextlib

from fastapi import FastAPI
import uvicorn

from config import app_config
from tools import di_container
from web.tools import router_registrator

config = app_config.config


app = FastAPI(
    debug=config.is_dev,
    title=config.app_name,
    version=config.app_version
)
router_registrator.register_routers(app)


if __name__ == "__main__":
    session_container = di_container.SessionContainer()
    repository_container = di_container.RepositoryContainer()
    # uow_container = di_container.UOWContainer()

    modules = [
        "services.auth_service",
        "services.user_service",
        "services.processor_service",
        "services.reporter_service",
    ]

    session_container.wire(modules=modules)
    repository_container.wire(modules=modules)
    # uow_container.wire(modules=modules)

    uvicorn.run(app, host=config.app_host, port=config.app_port)
