import uuid
from abc import ABC, abstractmethod

"""
Абстрактный класс для наследования моделей данных
"""


class AbstractReference(ABC):
    __uid: str = ""
    __name: str = ""

    def __init__(self, name: str = '', uid: str = ''):
        super().__init__()
        self.__name = name
        self.__uid = uid
        if not uid:
            self.__uid = str(uuid.uuid4())

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def name(self) -> str:
        return self.__name


