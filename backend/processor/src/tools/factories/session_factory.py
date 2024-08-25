from typing import AsyncGenerator

from sqlalchemy.ext import asyncio as alchemy_asyncio

from config import app_config
from interfaces import base_factory


class AlchemySessionFactory(base_factory.AbstractFactory):
    """
    Фабрика сессий SQLAlchemy
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """
        dsn = str(app_config.config.postgres_dsn)
        echo = True if app_config.config.is_dev else False

        engine = alchemy_asyncio.create_async_engine(dsn, echo=echo)

        self.session_maker = alchemy_asyncio.async_sessionmaker(
            autocommit=False, bind=engine
        )

    async def create(self) -> AsyncGenerator[alchemy_asyncio.AsyncSession, None]:
        """
        Создать объект асинхронной сессии
        :return: объект асинхронной сессии
        """

        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
