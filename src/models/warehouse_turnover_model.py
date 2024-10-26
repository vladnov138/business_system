from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel


class WarehouseTurnOverModel(BaseComparingByName):
    __warehouse: WarehouseModel = None
    __turnover: float = 0.0
    __nomenclature: NomenclatureModel = None
    __measurement_unit: MeasurementUnitModel = None

    @classmethod
    def create(cls, warehouse: WarehouseModel, turnover: float | int, nomenclature: NomenclatureModel,
               measurement_unit: MeasurementUnitModel):
        model = cls()
        model.warehouse = warehouse
        model.turnover = turnover
        model.nomenclature = nomenclature
        model.measurement_unit = measurement_unit
        return model

    @property
    def warehouse(self) -> WarehouseModel:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        ArgumentException.check_arg(value, WarehouseModel)
        self.__warehouse = value

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float | int):
        if isinstance(value, int):
            value = float(value)
        ArgumentException.check_arg(value, float)
        self.__turnover = value

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        ArgumentException.check_arg(value, NomenclatureModel)
        self.__nomenclature = value

    @property
    def measurement_unit(self) -> MeasurementUnitModel:
        return self.__measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnitModel):
        ArgumentException.check_arg(value, MeasurementUnitModel)
        self.__measurement_unit = value
