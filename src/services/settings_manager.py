import json
import os
from pathlib import Path

from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logger.log_level import LogLevel
from src.models.settings_model import Settings
from src.utils.file_reader import FileReader
from src.utils.json_model_encoder import JsonModelEncoder
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

    def __convert_format_reports(self, path):
        key = "format_reports"
        if key not in self.__data:
            raise OperationException(f"Ключ {key} отсутствует в файле настроек!")
        format_data = self.__data[key]
        result = {}
        for format in format_data:
            class_name = format_data[format]
            module = __import__(path.replace('/', '.'), fromlist=[class_name])
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
                report_format_key = "report_format"
                log_level_key = "log_level"
                if not isinstance(value, list) and not isinstance(value, dict) and field not in (report_format_key, log_level_key):
                    setattr(self.__settings, field, value)
                elif field in (report_format_key, log_level_key):
                    if field == report_format_key:
                        self.__settings.report_format = list(filter(lambda x: x.name == value, FormatReporting))[0]
                    else:
                        self.__settings.log_level = list(filter(lambda x: x.name == value, LogLevel))[0]
        self.__convert_format_reports(self.__settings.report_classes_folder)
        return self.__settings

    def open(self, file_name: str = ""):
        ArgumentException.check_arg(file_name, str)
        if file_name != "":
            self.__file_name = file_name
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            if not Path(self.__file_name).is_absolute():
                full_name = f"{parent_path}{os.sep}{self.__file_name}"
            else:
                full_name = self.__file_name
            self.__data = FileReader.read_json(full_name)
            return True
        except Exception as ex:
            self.__set_default_data()
            return False

    def save(self, file_name: str = ""):
        ArgumentException.check_arg(file_name, str)

        if file_name != "":
            self.__file_name = file_name

        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            if not Path(self.__file_name).is_absolute():
                full_name = f"{parent_path}{os.sep}{self.__file_name}"
            else:
                full_name = self.__file_name

            if os.path.exists(full_name):
                os.remove(full_name)

            result = json.dumps(self.__settings, cls=JsonModelEncoder, indent=2)

            with open(full_name, "w") as file:
                file.write(result)
            return True
        except Exception as ex:
            self.set_exception(ex)
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
                "business_type": "DEFDF", "correspondent_account": "13213213213",
                "recipe_folder": "docs/", "measurement_units_path": "resources/measurement_units.json",
                "date_format": "%Y-%m-%d"}
        self.__data = data
