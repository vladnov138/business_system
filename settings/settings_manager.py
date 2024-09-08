import json
import os
from pathlib import Path

from settings.settings_model import Settings


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
            file_path = Path(file_name)
            if not file_path.is_absolute():
                file_path = Path(os.curdir).joinpath(file_path).resolve()
            if not file_path.is_file():
                raise FileNotFoundError(f"File {file_path} does not exist")
            with file_path.open() as stream:
                self.__data = json.load(stream)
            return True
        except:
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

    def __default_settings(self):
        data = Settings()
        data.inn = "380080920202"
        data.organization_name = "Рога и копыта (default)"
        data.director_name = "Default default"
        data.bik = "999999999"
        data.account = "12312312312"
        data.business_type = "DEFDF"
        data.correspondent_account = "13213213213"
        return data