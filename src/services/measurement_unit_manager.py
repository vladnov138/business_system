import os
from pathlib import Path

from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.utils.file_reader import FileReader
from src.utils.path_utils import PathUtils


class MeasurementUnitManager:
    __file_name = "measurement_units.json"
    __data: dict = None
    __path_utils = PathUtils()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MeasurementUnitManager, cls).__new__(cls)
        return cls.instance

    def convert(self):
        if self.__data is None:
            raise AttributeError()
        units = []
        for key in self.__data.keys():
            base = None
            for unit in units:
                if unit.name == self.__data[key]['base']:
                    base = unit
                    break
            measurement_unit = MeasurementUnitModel(key, self.__data[key]['unit'], base)
            units.append(measurement_unit)
        return units

    def open(self, file_name: str = ""):
        ArgumentException.check_arg(file_name, str)
        if file_name != "":
            self.__file_name = file_name
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            measurement_units_file_parts = file_name.split('/')
            full_name = f"{parent_path}"
            for part in measurement_units_file_parts:
                full_name += f"{os.sep}{part}"
            self.__data = FileReader.read_json(full_name)
            self.__data = self.__data['measurements']
            return True
        except:
            self.__set_default_data()
            return False

    def __set_default_data(self):
        data = {"г": {"name": "г", "unit": 1, "base": None}, "кг": {"name": "кг", "unit": 1, "base": "г"}}
        self.__data = data
