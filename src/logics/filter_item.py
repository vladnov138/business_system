from src.abstract.filter_type import FilterType
from src.exceptions.argument_exception import ArgumentException


class FilterItem:
    __field: str = ""
    __type: FilterType = None
    __value: str = ""

    @classmethod
    def create(cls, field: str, filter_type: FilterType | str, value: str):
        instance = cls()
        instance.field = field
        instance.type = filter_type
        instance.value = value
        return instance

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__field = value.strip()

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: FilterType | str):
        if isinstance(value, str):
            try:
                value = FilterType(value)
            except:
                raise ArgumentException("Invalid parameter")
        ArgumentException.check_arg(value, FilterType)
        self.__type = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__value = value
