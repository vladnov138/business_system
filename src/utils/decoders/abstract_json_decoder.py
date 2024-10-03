from abc import ABC, abstractmethod


class AbstractJsonDecoder(ABC):
    _cls = None

    def __init__(self, cls):
        self._cls = cls

    @abstractmethod
    def decode(self, coded_obj: dict):
        pass

    @property
    def cls(self):
        return self._cls

    @cls.setter
    def cls(self, value):
        self._cls = value