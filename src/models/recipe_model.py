from src.abstract.base_comparing_by_uid import BaseComparingByUid
from src.exceptions.argument_exception import ArgumentException
from src.models.ingridient_model import IngridientModel


class RecipeModel(BaseComparingByUid):

    def __init__(self, name: str = '', ingridients: list[IngridientModel] = None, cooking_time_minutes: int = None, description: str = None):
        super().__init__(name)
        ArgumentException.check_arg(ingridients, list, True)
        if ingridients:
            for ingridient in ingridients:
                ArgumentException.check_arg(ingridient, IngridientModel, True)
        ArgumentException.check_arg(cooking_time_minutes, int, True)
        ArgumentException.check_arg(description, str, True)
        self.__ingridients = ingridients
        self.__cooking_time_minutes = cooking_time_minutes
        self.__description = description

    @property
    def ingridients(self):
        return self.__ingridients

    @property
    def cooking_time_minutes(self):
        return self.__cooking_time_minutes

    @property
    def description(self):
        return self.__description

    @ingridients.setter
    def ingridients(self, value: list[IngridientModel]):
        ArgumentException.check_arg(value, list)
        for ingridient in value:
            ArgumentException.check_arg(ingridient, IngridientModel)
        self.__ingridients = value

    @cooking_time_minutes.setter
    def cooking_time_minutes(self, value: int):
        ArgumentException.check_arg(value, int)
        ArgumentException.check_min_value(value, 0)
        self.__cooking_time_minutes = value

    @description.setter
    def description(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__description = value
