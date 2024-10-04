from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel


class IngridientModel(BaseComparingByName):
    __measurement_unit = None
    __amount = None

    @classmethod
    def create(cls, name: str, measurement_unit: MeasurementUnitModel, amount: float):
        model = cls()
        model.name = name
        model.measurement_unit = measurement_unit
        model.amount = amount
        return model


    def __cvt_unit_to_float(self, amount: (int | float)):
        if isinstance(amount, int):
            amount = float(amount)
        return amount

    @property
    def measurement_unit(self):
        return self.__measurement_unit

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        value = self.__cvt_unit_to_float(value)
        ArgumentException.check_arg(value, float)
        ArgumentException.check_min_value(value, 1)
        self.__amount = value

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnitModel):
        ArgumentException.check_arg(value, MeasurementUnitModel)
        self.__measurement_unit = value