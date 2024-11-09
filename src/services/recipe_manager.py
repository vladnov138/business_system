import os
from pathlib import Path

from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.data.data_repository import DataRepository
from src.exceptions.argument_exception import ArgumentException
from src.utils.file_reader import FileReader
from src.utils.parser import Parser
from src.utils.path_utils import PathUtils


class RecipeManager(AbstractLogic):
    __recipe_folder = "docs/"
    __data: list = None
    __path_utils = PathUtils()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RecipeManager, cls).__new__(cls)
        return cls.instance

    def convert(self, measurement_units, repository: DataRepository):
        if self.__data is None:
            raise AttributeError()
        recipes = []
        for recipe_raw_text in self.__data:
            recipe = Parser.parse_recipe_from_md(recipe_raw_text, measurement_units, repository)
            recipes.append(recipe)
        return recipes

    def open(self, recipe_folder: str = ""):
        ArgumentException.check_arg(recipe_folder, str)
        if recipe_folder != "":
            self.__recipe_folder = recipe_folder
        try:
            current_path = Path(__file__).resolve()
            parent_path = self.__path_utils.get_parent_directory(current_path, levels_up=3)
            full_name = f"{parent_path}{os.sep}{recipe_folder}"
            files = self.__path_utils.get_files_by_path(full_name)
            recipes_raw_texts = []
            for file in files:
                text = FileReader.read_file(file)
                recipes_raw_texts.append(text)
            self.__data = recipes_raw_texts
            return True
        except:
            self.__set_default_data()
            return False

    def __set_default_data(self):
        data = []
        self.__data = data

    def set_exception(self, ex: Exception):
        self.set_exception(ex)

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)
        if "nomenclature" not in kwargs or "data":
            raise ArgumentException("nomenclature and data is required")
        nomenclature = kwargs["nomenclature"]
        repository: DataRepository = kwargs["data"]
        recipe_key = repository.recipe_key()
        recipes = repository.data[recipe_key]
        match(type):
            case EventType.CHANGE_NOMENCLATURE:
                for recipe in recipes:
                    if nomenclature in recipe:
                        recipe["nomenclature"] = nomenclature
                        recipes[recipes.index(recipe)] = recipe
                        break