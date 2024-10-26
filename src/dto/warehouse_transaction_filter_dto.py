from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel


class WarehouseTransactionFilterDto(BaseComparingByName):
    __warehouse: WarehouseModel = None
    __nomenclature: NomenclatureModel = None

    def __init__(self):
        pass

    @classmethod
    def create(cls, warehouse: WarehouseModel, nomenclature: NomenclatureModel):
        filter_dto = cls()
        filter_dto.warehouse = warehouse
        filter_dto.nomenclature = nomenclature
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