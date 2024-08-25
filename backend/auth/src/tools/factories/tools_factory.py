from interfaces import base_factory
from tools import jwt_helper


class JWTHelperFactory(base_factory.AbstractFactory):
    """
    Фабрика вспомогательного класса для работы с JWT-токенами
    """

    def create(self) -> jwt_helper.JWTHelper:
        """
        Создать объект вспомогательного класса для работы с JWT
        :return: объект класса для работы с JWT
        """

        return jwt_helper.JWTHelper()
