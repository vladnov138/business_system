from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

from src.exceptions.argument_exception import ArgumentException

"""
Абстрактный класс для наследования моделей данных
"""


class AbstractReference(ABC):
    _uid: str = ""
    _name: str = ""

    def __init__(self):
        super().__init__()
        self._uid = str(uuid.uuid4())

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @name.setter
    def name(self, value: str = ''):
        ArgumentException.check_arg(value, str, True)
        self._name = value

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    def __str__(self) -> str:
        return self._uid