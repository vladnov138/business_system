from src.abstract.base_comparing_by_name import BaseComparingByName


class StorageModel(BaseComparingByName):

    @classmethod
    def create(cls, name: str):
        model = cls()
        model.name = name
        return model
