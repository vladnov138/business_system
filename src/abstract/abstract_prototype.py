from abc import ABC, abstractmethod

from src.abstract.filter_type import FilterType
from src.exceptions.argument_exception import ArgumentException


class AbstractPrototype(ABC):
    __data = []

    def __init__(self, source: list):
        super().__init__()
        ArgumentException.check_arg(source, list)
        self.__data = source
        self._conditions = {
            FilterType.EQUAL: lambda searched_text, text: searched_text == text,
            FilterType.LIKE: lambda searched_text, text: searched_text in text
        }

    @abstractmethod
    def create(self, filter_item):
        pass

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list):
        self.__data = value