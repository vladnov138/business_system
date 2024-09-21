from src.abstract.base_comparing_by_uid import BaseComparingByUid


class NomenclatureGroupModel(BaseComparingByUid):
    """
        Default группа - сырье
        """
    @staticmethod
    def default_group_source():
        item = NomenclatureGroupModel("Сырьё")
        return item

    """
    Default группа - заморозка
    """
    @staticmethod
    def default_group_cold():
        item = NomenclatureGroupModel("Заморозка")
        return item
