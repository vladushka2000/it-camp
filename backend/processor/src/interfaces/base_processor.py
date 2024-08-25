import abc


class AbstractProcessor(abc.ABC):
    """
    Абстрактный класс обработчика магнитограммы
    """

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> any:
        """
        Обработать магнитограмму
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_processed_image(self, *args, **kwargs) -> any:
        """
        Получить изображение обработанной магнитограммы
        """

        raise NotImplementedError
