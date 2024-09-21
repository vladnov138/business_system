from src.abstract.base_comparing_by_name import BaseComparingByName
from src.models.measurement_unit_model import MeasurementUnitModel


class Ingridient(BaseComparingByName):

    def __init__(self, name: str, measurement_unit: MeasurementUnitModel, amount: float):
        super().__init__(name)
        self.__measurement_unit = measurement_unit
        self.__amount = amount

    @property
    def measurement_unit(self):
        return self.__measurement_unit

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        self.__amount = value

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnitModel):
        self.__measurement_unit = value