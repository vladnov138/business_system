from datetime import datetime

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.logics.warehouse_filter_item import WarehouseFilterItem
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel


class WarehouseTransactionFilterDto(BaseComparingByName):
    __items: list[WarehouseFilterItem] = []

    def __init__(self):
        pass

    @classmethod
    def create(cls, items: list[WarehouseFilterItem]):
        filter_dto = cls()
        filter_dto.items = items
        return filter_dto

    @property
    def items(self) -> list[WarehouseFilterItem]:
        return self.__items

    @items.setter
    def items(self, value: list[WarehouseFilterItem]):
        for item in value:
            ArgumentException.check_arg(item, WarehouseFilterItem, True)
        self.__items = value
