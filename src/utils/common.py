from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.base_comparing_by_uid import BaseComparingByUid


class Common:
    def get_models_dict(self):
        models = {}
        for inheritor in BaseComparingByName.__subclasses__():
            models[inheritor.__name__] = inheritor
        for inheritor in BaseComparingByUid.__subclasses__():
            models[inheritor.__name__] = inheritor
        return models