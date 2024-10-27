from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.filter_type import FilterType
from src.exceptions.argument_exception import ArgumentException
from src.logics.filter_item import FilterItem


class FilterDto(BaseComparingByName):
    __items: list[FilterItem] = []

    def __init__(self):
        pass

    @classmethod
    def create(cls, items: list[FilterItem]):
        filter_dto = cls()
        filter_dto.items = items
        return filter_dto

    @property
    def items(self) -> list[FilterItem]:
        return self.__items

    @items.setter
    def items(self, value: list[FilterItem]):
        for item in value:
            ArgumentException.check_arg(item, FilterItem)
        self.__items = value