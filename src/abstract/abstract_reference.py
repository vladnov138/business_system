from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

from src.exceptions.argument_exception import ArgumentException

"""
Абстрактный класс для наследования моделей данных
"""


class AbstractReference(ABC):
    __uid: str = ""
    _name: str = ""

    def __init__(self, name: str = '', uid: str = ''):
        super().__init__()
        ArgumentException.check_arg(name, str)
        ArgumentException.check_arg(uid, str)
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
        ArgumentException.check_arg(value, str)
        self._name = value

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    def __str__(self) -> str:
        return self.__uid