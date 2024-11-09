from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):

    @abstractmethod
    def update(self, dateblock: datetime):
        pass