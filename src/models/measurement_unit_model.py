from __future__ import annotations

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException


class MeasurementUnitModel(BaseComparingByName):
    __unit: float = 0
    __base_measure_unit: MeasurementUnitModel = None

    @classmethod
    def create(cls, name: str, unit: float, base_measure_unit: MeasurementUnitModel=None):
        model = cls()
        model.name = name
        model.unit = unit
        model.base_measure_unit = base_measure_unit
        return model

    def __cvt_unit_to_float(self, unit: (int | float)):
        if isinstance(unit, int):
            unit = float(unit)
        return unit

    @property
    def unit(self):
        return self.__unit

    @property
    def base_measure_unit(self):
        return self.__base_measure_unit

    @unit.setter
    def unit(self, value: float):
        value = self.__cvt_unit_to_float(value)
        ArgumentException.check_arg(value, float)
        self.__unit = value

    @base_measure_unit.setter
    def base_measure_unit(self, value: MeasurementUnitModel):
        ArgumentException.check_arg(value, MeasurementUnitModel, True)
        self.__base_measure_unit = value