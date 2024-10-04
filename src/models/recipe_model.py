from src.abstract.base_comparing_by_uid import BaseComparingByUid
from src.exceptions.argument_exception import ArgumentException
from src.models.ingridient_model import IngridientModel


class RecipeModel(BaseComparingByUid):
    __ingridients = None
    __cooking_time_minutes = None
    __description = None

    @classmethod
    def create(cls, name: str, ingridients: list[IngridientModel], cooking_time_minutes: int, description: str):
        model = cls()
        model.name = name
        model.ingridients = ingridients
        model.cooking_time_minutes = cooking_time_minutes
        model.description = description
        return model

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
