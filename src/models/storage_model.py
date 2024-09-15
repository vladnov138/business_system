from src.abstract_reference import AbstractReference


class StorageModel(AbstractReference):
    def __eq__(self, other):
        if not isinstance(other, StorageModel):
            return False
        return self._name == other._name

    def __ne__(self, other):
        return not self == other