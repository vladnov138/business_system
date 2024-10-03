from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel


class NomenclatureModel(BaseComparingByName):
    __full_name: str = None
    __nomenclature_group: NomenclatureGroupModel = None
    __measurement_unit: MeasurementUnitModel = None

    def __init__(self, name: str = '', nomenclature_group: NomenclatureGroupModel = None, measurement_unit: MeasurementUnitModel = None,
                 full_name: str = None):
        super().__init__(name)
        ArgumentException.check_arg(nomenclature_group, NomenclatureGroupModel, True)
        ArgumentException.check_arg(measurement_unit, MeasurementUnitModel, True)
        ArgumentException.check_arg(full_name, str, True)
        self.__nomenclature_group = nomenclature_group
        self.__measurement_unit = measurement_unit
        self.__full_name = full_name

    @staticmethod
    def default_flour_nomenclature(group: NomenclatureGroupModel, measurement_unit: MeasurementUnitModel):
        nomenclature = NomenclatureModel("Мука", group, measurement_unit)
        return nomenclature

    @staticmethod
    def default_ice_nomenclature(group: NomenclatureGroupModel, measurement_unit: MeasurementUnitModel):
        nomenclature = NomenclatureModel("Лёд", group, measurement_unit)
        return nomenclature


    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str = None):
        ArgumentException.check_arg(value, str, True)
        if value:
            ArgumentException.check_max_len(value, 255)
        self.__full_name = value

    @property
    def measurement_unit(self):
        return self.__measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnitModel):
        ArgumentException.check_arg(value, MeasurementUnitModel)
        self.__measurement_unit = value

    @property
    def nomenclature_group(self):
        return self.__nomenclature_group

    @nomenclature_group.setter
    def nomenclature_group(self, value: NomenclatureGroupModel):
        ArgumentException.check_arg(value, NomenclatureModel)
        self.__nomenclature_group = value