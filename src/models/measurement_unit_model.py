class MeasurementUnitModel:
    __name: str = ""
    __unit: int = 0
    __base_measure_unit = None

    def __init__(self, name: str, unit: int, base_measure_unit=None):
        self.__name = name
        self.__unit = unit
        self.__base_measure_unit = base_measure_unit

    @property
    def name(self):
        return self.__name

    @property
    def unit(self):
        return self.__unit

    @property
    def base_measure_unit(self):
        return self.__base_measure_unit