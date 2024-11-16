import json
import os
from pathlib import Path

from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.data.data_repository import DataRepository
from src.exceptions.argument_exception import ArgumentException
from src.utils.file_reader import FileReader
from src.utils.json_model_encoder import JsonModelEncoder
from src.utils.path_utils import PathUtils


class DataManager(AbstractLogic):
    __file_name = "settings.json"
    __data: dict = None
    __path_utils = PathUtils()

    def __init__(self, repository: DataRepository):
        self.__data = repository.data

    def save(self, file_name: str):
        ArgumentException.check_arg(file_name, str)
        if file_name == "":
            file_name = self.__file_name
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            if not Path(file_name).is_absolute():
                full_name = f"{parent_path}{os.sep}{file_name}"
            else:
                full_name = file_name

            if os.path.exists(full_name):
                os.remove(full_name)

            result = json.dumps(self.__data, cls=JsonModelEncoder, indent=2)
            with open(full_name, "w") as file:
                file.write(result)
            return True
        except Exception as ex:
            self.set_exception(ex)
            return False

    def load(self, file_name: str):
        ArgumentException.check_arg(file_name, str)
        if file_name == "":
            file_name = self.__file_name
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            if not Path(file_name).is_absolute():
                full_name = f"{parent_path}{os.sep}{file_name}"
            else:
                full_name = file_name

            if os.path.exists(full_name):
                os.remove(full_name)

            result = FileReader.read_json(full_name)
            return result
        except Exception as ex:
            self.set_exception(ex)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)