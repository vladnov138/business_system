from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.filter_type import FilterType


class FilterDto(BaseComparingByName):
    __type: FilterType = None

    def __init__(self):
        pass

    @classmethod
    def create(cls, uid, name, type):
        filter_dto = cls()
        filter_dto.uid = uid
        filter_dto.name = name
        filter_dto.type = FilterType(type)
        return filter_dto

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: FilterType | str):
        if isinstance(value, str):
            value = FilterType(value)
        self.__type = value