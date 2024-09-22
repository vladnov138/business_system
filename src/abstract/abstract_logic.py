from abc import ABC, abstractmethod

from src.exceptions.argument_exception import ArgumentException


class AbstractLogic(ABC):
    """
    Абстрактный класс для обработки логики
    """
    __error_text: str = ""

    @property
    def error_text(self) -> str:
        """
        Описание ошибки
        """
        return self.__error_text.strip()

    @error_text.setter
    def error_text(self, message: str):
        ArgumentException.check_arg(message, str)
        self.__error_text = message.strip()

    @property
    def is_error(self) -> bool:
        """
        Флаг. Есть ошибка
        """
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    @abstractmethod
    def set_exception(self, ex: Exception):
        """
        Абстрактный метод для загрузки и обработки исключений
        """
        pass
