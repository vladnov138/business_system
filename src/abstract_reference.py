import inspect
import uuid
from abc import ABC, abstractmethod

from src.exceptions.argument_exception import ArgumentException
from src.utils.checker import check_arg

"""
Абстрактный класс для наследования моделей данных
"""


class AbstractReference(ABC):
    __uid: str = ""
    _name: str = ""

    def __init__(self, name: str = '', uid: str = ''):
        super().__init__()
        check_arg(name, str)
        check_arg(uid, str)
        self._name = name
        self.__uid = uid
        if not uid:
            self.__uid = str(uuid.uuid4())

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        check_arg(value, str)
        self._name = value

    def __eq__(self, other):
        if not isinstance(other, AbstractReference):
            return False
        return self.__uid == other.__uid

    def __ne__(self, other):
        if not isinstance(other, AbstractReference):
            return True
        return self.__uid != other.__uid
