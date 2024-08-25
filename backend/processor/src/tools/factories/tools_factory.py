from interfaces import base_factory
from tools.processors import processor, process_result_truncator


class ProcessorFactory(base_factory.AbstractFactory):
    """
    Фабрика обработчиков магнитограмм
    """

    def create(self) -> processor.Processor:
        """
        Создать объект обработчика
        :return: обработчик магнитограмм
        """

        return processor.Processor()


class TruncatorFactory(base_factory.AbstractFactory):
    """
    Фабрика форматтера результата обработчика
    """

    def create(self) -> process_result_truncator.ProcessResultTrancutor:
        """
        Создать объект утилиты
        :return: утилита
        """

        return process_result_truncator.ProcessResultTrancutor()
