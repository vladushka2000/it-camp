from sqlalchemy import select, or_

from dto import user_dto
from interfaces import base_repository
from repositories.models import user_model
from tools import exceptions


class UserRepository(
    base_repository.AbstractAlchemyRepository, base_repository.CreateMixin, base_repository.RetrieveMixin
):
    """
    Репозиторий для работы с данными пользователя
    """

    def create(self, user: user_dto.UserDTO) -> None:
        """
        Создать запись пользователя
        :param user: объект пользователя
        """

        user_db_model = user_model.User(
            id=user.id,
            name=user.name,
            hashed_password=user.password,
            role_id=user.role,
            created_at=user.created_at,
        )

        self.session.add(user_db_model)

    async def retrieve(
        self, user_name: str = None, user_id: str = None
    ) -> user_dto.UserDTO | None:
        """
        Получить запись пользователя
        :param user_name: имя пользователя
        :param user_id: идентификатор пользователя
        """

        if user_name is None and user_id is None:
            raise exceptions.UserFaultException("Не передан параметр для получения пользователя")

        filter_criteries = (
            user_model.User.name == user_name if user_name else None,
            user_model.User.id == user_id if user_id else None,
        )

        query = select(user_model.User).filter(
            or_(*[criteria for criteria in filter_criteries if criteria is not None])
        )
        result = await self.session.execute(query)
        result = result.scalars().first()

        if result is None:
            return

        return user_dto.UserDTO(
            id=result.id,
            name=result.name,
            password=result.hashed_password,
            role=result.role_id,
            created_at=result.created_at,
        )
