import datetime

from sqlalchemy import select, and_

from dto import history_dto
from interfaces import base_repository
from repositories.models import history_model


class HistoryRepository(
    base_repository.AbstractAlchemyRepository, base_repository.CreateMixin, base_repository.RetrieveMixin
):
    """
    Репозиторий для работы с историей загрузок
    """

    def create(self, history: history_dto.HistoryDTO) -> None:
        """
        Создать запись истории
        :param history: объект записи истории
        """

        history_db_model = history_model.History(
            id=str(history.id),
            magnetogram_id=str(history.magnetogram_id),
            action_type_id=str(history.action_type_id),
            user_name=history.user_name,
            date=history.date,
        )

        self.session.add(history_db_model)

    async def retrieve(
        self,
        date_to: datetime.datetime | None = None,
        date_from: datetime.datetime | None = None
    ) -> list[history_dto.HistoryDTO] | None:
        """
        Получить запись истории
        :param date_to: дата конца поиска
        :param date_from: дата начала поиска
        :return: список отчетов
        """

        query = select(history_model.History)

        filter_criteries = (
            history_model.History.date >= date_from,
            history_model.History.date <= date_to
        )

        query = query.filter(
            and_(*filter_criteries)
        )

        result = await self.session.execute(query)
        result = result.scalars().all()

        if not result:
            return

        return [
            history_dto.HistoryDTO(
                id=history.id,
                magnetogram_id=history.magnetogram_id,
                action_type_id=history.action_type_id,
                user_name=history.user_name,
                date=history.date
            )
            for history in result
        ]
