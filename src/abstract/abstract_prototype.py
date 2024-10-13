from abc import ABC, abstractmethod

from src.exceptions.argument_exception import ArgumentException


class AbstractPrototype(ABC):
    __data = []

    def __init__(self, source: list):
        super().__init__()
        ArgumentException.check_arg(source, list)
        self.__data = source

    @abstractmethod
    def create(self, data: list, filter_dto):
        ArgumentException.check_arg(data, list)

        # instance = AbstractPrototype(data)
        # return instance

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list):
        self.__data = value