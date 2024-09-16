from src.abstract_reference import AbstractReference


class BaseComparingByName(AbstractReference):
    def __eq__(self, other):
        if not isinstance(other, AbstractReference):
            return False
        return self.name == other.name

    def __ne__(self, other):
        return not self == other