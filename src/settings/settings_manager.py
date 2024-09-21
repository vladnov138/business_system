import json
import os
from pathlib import Path

from src.models.settings_model import Settings


class SettingsManager:
    __file_name = "settings.json"
    __settings: Settings = Settings()
    __data: dict = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    # def __init__(self) -> None:
    #     self.__settings = self.__default_settings()

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

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Invalid argument")
        if file_name != "":
            self.__file_name = file_name
        try:
            current_path_info = os.path.split(__file__)
            current_path: str = current_path_info[0]
            current_path = current_path[:current_path.rfind('/')]
            current_path = current_path[:current_path.rfind('/')]
            full_name = f"{current_path}{os.sep}{self.__file_name}"
            with open(full_name) as stream:
                self.__data = json.load(stream)
            return True
        except:
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
