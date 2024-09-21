from src.abstract.base_comparing_by_uid import BaseComparingByUid
from src.models.ingridient import Ingridient


class Recipe(BaseComparingByUid):

    def __init__(self, name: str, ingridients: list[Ingridient], cooking_time_minutes: int, description: str):
        super().__init__(name)
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
    def ingridients(self, value: list[Ingridient]):
        self.__ingridients = value

    @cooking_time_minutes.setter
    def cooking_time_minutes(self, value: int):
        self.__cooking_time_minutes = value

    @description.setter
    def description(self, value: str):
        self.__description = value
