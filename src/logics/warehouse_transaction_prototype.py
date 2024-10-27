from src.abstract.abstract_prototype import AbstractPrototype
from src.abstract.date_filter_type import DateFilterType
from src.abstract.period_filter_item import PeriodFilterItem
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.filter_item import FilterItem
from src.logics.warehouse_filter_item import WarehouseFilterItem


class WarehouseTransactionPrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)
        self.__date_conditions = {
            DateFilterType.EQUAL: lambda searched_date, date: searched_date.date() == date.date(),
            DateFilterType.AFTER: lambda searched_date, date: searched_date.date() < date.date(),
            DateFilterType.BEFORE: lambda searched_date, date: searched_date.date() > date.date()
        }

    def __filter_period(self, field: str, filter_item: PeriodFilterItem) -> list:
        if filter_item is None:
            return self.data
        condition = self.__date_conditions.get(filter_item.filter_type) or None
        if condition is None:
            raise OperationException("Invalid filter type")
        result = []
        for item in self.data:
            field_date = getattr(item, field)
            if field_date is None:
                raise OperationException("Invalid field")
            if condition(filter_item.date, field_date):
                result.append(item)
        return result

    def __filter(self, field: str, filter_item: FilterItem):
        if filter_item is None:
            return self.data
        condition = self._conditions.get(filter_item.type) or None
        if condition is None:
            raise OperationException("Invalid filter type")
        result = []
        for item in self.data:
            field_model = getattr(item, field)
            field_model_value = getattr(field_model, filter_item.field)
            if field_model_value is None:
                raise OperationException("Invalid field")
            if condition(filter_item.value, field_model_value):
                result.append(item)
        return result

    def create(self, filter_item: WarehouseFilterItem):
        ArgumentException.check_arg(filter_item, WarehouseFilterItem)
        if filter_item.warehouse_item:
            self.data = self.__filter("warehouse", filter_item.warehouse_item)
        if filter_item.nomenclature_item:
            self.data = self.__filter("nomenclature", filter_item.nomenclature_item)
        if filter_item.period:
            self.data = self.__filter_period("period", filter_item.period)
        prototype = WarehouseTransactionPrototype(self.data)
        return prototype