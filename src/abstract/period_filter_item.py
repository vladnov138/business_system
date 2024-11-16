from datetime import datetime

from src.abstract.date_filter_type import DateFilterType
from src.exceptions.argument_exception import ArgumentException


class PeriodFilterItem:
    __date: datetime = None
    __filter_type: DateFilterType = None

    @classmethod
    def create(cls, date: datetime, filter_type: DateFilterType):
        instance = cls()
        instance.date = date
        instance.filter_type = filter_type
        return instance

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value: datetime):
        ArgumentException.check_arg(value, datetime, True)
        self.__date = value

    @property
    def filter_type(self):
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, value: DateFilterType | str):
        if isinstance(value, str):
            try:
                value = DateFilterType(value)
            except:
                raise ArgumentException("Invalid parameter")
        ArgumentException.check_arg(value, DateFilterType, True)
        self.__filter_type = value