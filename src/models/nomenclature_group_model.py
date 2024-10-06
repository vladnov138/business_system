from src.abstract.base_comparing_by_uid import BaseComparingByUid


class NomenclatureGroupModel(BaseComparingByUid):

    @classmethod
    def create(cls, name: str):
        model = cls()
        model.name = name
        return model

    @staticmethod
    def default_group_source():
        """
        Default группа - сырье
        """
        item = NomenclatureGroupModel.create("Сырьё")
        return item


    @staticmethod
    def default_group_cold():
        """
        Default группа - заморозка
        """
        item = NomenclatureGroupModel.create("Заморозка")
        return item
