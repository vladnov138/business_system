from abc import ABC

from src.abstract.abstract_reference import AbstractReference


class BaseComparingByName(AbstractReference, ABC):
    def __eq__(self, other):
        if not isinstance(other, AbstractReference):
            return False
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.uid)