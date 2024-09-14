from __future__ import annotations

from src.abstract_reference import AbstractReference
from src.utils.checker import check_arg


class MeasurementUnitModel(AbstractReference):
    __unit: float = 0
    __base_measure_unit: MeasurementUnitModel = None

    def __init__(self, name: str, unit: float, base_measure_unit: MeasurementUnitModel=None):
        super().__init__(name)
        unit = self.__cvt_unit_to_float(unit)
        check_arg(unit, float)
        check_arg(base_measure_unit, MeasurementUnitModel, True)
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
        check_arg(value, float)
        self.__unit = value

    @base_measure_unit.setter
    def base_measure_unit(self, value: MeasurementUnitModel):
        check_arg(value, MeasurementUnitModel)
        self.__base_measure_unit = value

    def __eq__(self, other):
        if not isinstance(other, MeasurementUnitModel):
            return False
        return self._name == other._name

    def __ne__(self, other):
        if not isinstance(other, MeasurementUnitModel):
            return True
        return self._name != other._name