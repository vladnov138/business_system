from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_model import NomenclatureModel


class IngridientModel(BaseComparingByName):
    __measurement_unit = None
    __nomenclature = None
    __amount = None

    @classmethod
    def create(cls, nomenclature: NomenclatureModel, amount: float):
        model = cls()
        model.nomenclature = nomenclature
        model.amount = amount
        return model

    def __cvt_unit_to_float(self, amount: (int | float)):
        if isinstance(amount, int):
            amount = float(amount)
        return amount

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        value = self.__cvt_unit_to_float(value)
        ArgumentException.check_arg(value, float)
        ArgumentException.check_min_value(value, 1)
        self.__amount = value

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        ArgumentException.check_arg(value, NomenclatureModel)
        self.__nomenclature = value
