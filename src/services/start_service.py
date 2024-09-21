import os

from src.data.data_repository import DataRepository
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.settings_model import Settings
from src.utils.file_reader import FileReader
from src.utils.parser import Parser
from src.utils.path_utils import PathUtils


class StartService:
    __repository: DataRepository = None
    __settings: Settings = None

    def __init__(self, repository: DataRepository, settings: Settings):
        super().__init__()
        self.__repository = repository
        self.__settings = settings

    def __create_nomenclature_groups(self):
        list = [NomenclatureGroupModel.default_group_cold(), NomenclatureGroupModel.default_group_source() ]
        self.__repository.data[DataRepository.group_key()] = list

    def __create_measurement_units(self):
        current_path = PathUtils.get_parent_directory(__file__, levels_up=3)
        measurement_units_file = self.__settings.measurement_units_path
        measurement_units_file_parts = measurement_units_file.split('/')
        full_name = f"{current_path}"
        for part in measurement_units_file_parts:
            full_name += f"{os.sep}{part}"
        data = FileReader.read_json(full_name)
        data = data["measurements"]
        units = Parser.parse_measurement_units_from_dict(data)
        self.__repository.data[DataRepository.measurement_unit_key()] = units

    def __create_nomenclature(self):
        groups_list = self.__repository.data[DataRepository.group_key()]
        group = groups_list[1]
        measurements = self.__repository.data[DataRepository.measurement_unit_key()]
        measurement_unit = measurements[1]
        nomenclature = NomenclatureModel("Мука", group, measurement_unit)
        nomenclatures = [nomenclature]
        group = groups_list[0]
        measurement_unit = measurements[0]
        nomenclature = NomenclatureModel("Лёд", group, measurement_unit)
        nomenclatures.append(nomenclature)
        self.__repository.data[DataRepository.nomenclature_key()] = nomenclatures

    def __create_recipe(self):
        current_path = PathUtils.get_parent_directory(__file__, levels_up=3)
        docs_folder = self.__settings.recipe_folder
        full_name = f"{current_path}{os.sep}{docs_folder}"
        files = PathUtils.get_files_by_path(full_name)
        recipes = []
        for file in files:
            text = FileReader.read_file(file)
            recipe = Parser.parse_recipe_from_md(text, self.__repository.data[DataRepository.measurement_unit_key()])
            recipes.append(recipe)
        self.__repository.data[DataRepository.recipe_key()] = recipes


    """
    Первый старт
    """
    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurement_units()
        self.__create_nomenclature()
        self.__create_recipe()
