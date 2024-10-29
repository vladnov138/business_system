from src.abstract.period_filter_item import PeriodFilterItem
from src.exceptions.argument_exception import ArgumentException
from src.logics.filter_item import FilterItem


class WarehouseFilterItem:
    __warehouse_item: FilterItem = None
    __nomenclature_item: FilterItem = None
    __period: PeriodFilterItem = None

    @property
    def warehouse_item(self) -> FilterItem:
        return self.__warehouse_item

    @warehouse_item.setter
    def warehouse_item(self, value: FilterItem):
        ArgumentException.check_arg(value, FilterItem, True)
        self.__warehouse_item = value

    @property
    def nomenclature_item(self) -> FilterItem:
        return self.__nomenclature_item

    @nomenclature_item.setter
    def nomenclature_item(self, value: FilterItem):
        ArgumentException.check_arg(value, FilterItem, True)
        self.__nomenclature_item = value

    @property
    def period(self) -> PeriodFilterItem:
        return self.__period

    @period.setter
    def period(self, value: PeriodFilterItem):
        ArgumentException.check_arg(value, PeriodFilterItem, True)
        self.__period = value