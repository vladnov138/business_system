from datetime import datetime

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel


class WarehouseTransactionFilterDto(BaseComparingByName):
    __warehouse: WarehouseModel = None
    __nomenclature: NomenclatureModel = None
    __date_from: datetime = None
    __date_to: datetime = None

    def __init__(self):
        pass

    @classmethod
    def create(cls, warehouse: WarehouseModel, nomenclature: NomenclatureModel, date_from: datetime, date_to: datetime):
        filter_dto = cls()
        filter_dto.warehouse = warehouse
        filter_dto.nomenclature = nomenclature
        filter_dto.date_from = date_from
        filter_dto.date_to = date_to
        return filter_dto

    @property
    def warehouse(self):
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        ArgumentException.check_arg(value, WarehouseModel, True)
        self.__warehouse = value

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        ArgumentException.check_arg(value, NomenclatureModel, True)
        self.__nomenclature = value

    @property
    def date_from(self):
        return self.__date_from

    @date_from.setter
    def date_from(self, value: datetime):
        ArgumentException.check_arg(value, datetime, True)
        self.__date_from = value

    @property
    def date_to(self):
        return self.__date_to

    @date_to.setter
    def date_to(self, value: datetime):
        ArgumentException.check_arg(value, datetime, True)
        self.__date_to = value