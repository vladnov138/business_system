import os
from pathlib import Path

from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.models.settings_model import Settings
from src.utils.file_reader import FileReader
from src.utils.path_utils import PathUtils


class SettingsManager:
    __file_name = "settings.json"
    __settings: Settings = Settings()
    __data: dict = None
    __path_utils = PathUtils()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    def __convert_report_formats(self):
        key = "format_reports"
        format_data = self.__data[key]
        result = {}
        for format in format_data:
            class_name = format_data[format]
            module = __import__('src.reports', fromlist=[class_name])
            report_class_file = getattr(module, class_name)
            classes = dir(report_class_file)
            capitalized_class_name = class_name.title().replace('_', '')
            if capitalized_class_name not in classes:
                raise OperationException(f"Класс отчета {class_name} не реализован!")
            report_class = getattr(report_class_file, capitalized_class_name)
            format_name = list(filter(lambda x: x.name == format, FormatReporting))[0]
            result[format_name] = report_class
        setattr(self.__settings, key, result)

    def convert(self):
        if self.__data is None:
            raise AttributeError()
        fields = dir(self.__settings)
        for field in fields:
            keys = list(filter(lambda x: x == field, self.__data.keys()))
            if len(keys) != 0:
                value = self.__data[field]
                if not isinstance(value, list) and not isinstance(value, dict):
                    setattr(self.__settings, field, value)
        self.__convert_report_formats()
        return self.__settings

    def open(self, file_name: str = ""):
        ArgumentException.check_arg(file_name, str)
        if file_name != "":
            self.__file_name = file_name
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            # full_name = f"{parent_path}{os.sep}{self.__file_name}"
            full_name = os.path.join(parent_path, self.__file_name)
            self.__data = FileReader.read_json(full_name)
            return True
        except Exception as ex:
            self.__set_default_data()
            return False

    # Настройки
    @property
    def settings(self):
        return self.__settings

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value: dict):
        if isinstance(value, dict):
            self.__data = value

    def __set_default_data(self):
        data = {"inn": "380080920202", "organization_name": "Рога и копыта (default)",
                "director_name": "Default default", "bik": "999999999", "account": "12312312312",
                "business_type": "DEFDF", "correspondent_account": "13213213213"}
        self.__data = data
