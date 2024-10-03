from __future__ import annotations

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException


class MeasurementUnitModel(BaseComparingByName):
    __unit: float = 0
    __base_measure_unit: MeasurementUnitModel = None

    def __init__(self, name: str='', unit: float=None, base_measure_unit: MeasurementUnitModel=None):
        super().__init__(name)
        unit = self.__cvt_unit_to_float(unit)
        ArgumentException.check_arg(unit, float, True)
        ArgumentException.check_arg(base_measure_unit, MeasurementUnitModel, True)
        self.__unit = unit
        self.__base_measure_unit = base_measure_unit

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