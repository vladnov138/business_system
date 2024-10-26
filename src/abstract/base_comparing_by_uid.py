from __future__ import annotations

from abc import ABC

from src.abstract.abstract_reference import AbstractReference


class BaseComparingByUid(AbstractReference, ABC):
    def __eq__(self, other: AbstractReference):
        if not isinstance(other, AbstractReference):
            return False
        return self.uid == other.uid

    def __ne__(self, other: AbstractReference):
        return not self == other

    def __hash__(self):
        return hash(self.uid)