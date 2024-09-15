from src.abstract_reference import AbstractReference


class NomenclatureGroupModel(AbstractReference):
    def __eq__(self, other):
        if not isinstance(other, NomenclatureGroupModel):
            return False
        return self.uid == other.uid

    def __ne__(self, other):
        return not self == other