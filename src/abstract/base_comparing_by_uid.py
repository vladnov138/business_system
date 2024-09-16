from __future__ import annotations

from src.abstract_reference import AbstractReference


class BaseComparingByUid(AbstractReference):
    def __eq__(self, other: AbstractReference):
        if not isinstance(other, AbstractReference):
            return False
        return self.uid == other.uid

    def __ne__(self, other: AbstractReference):
        return not self == other