import json
import os
import re

from src.data.data_repository import DataRepository
from src.models.ingridient import Ingridient
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe import Recipe
from src.settings.settings_manager import SettingsManager


class StartService:
    __repository: DataRepository = None
    __settings_manager: SettingsManager = None

    def __init__(self, repository: DataRepository, settings_manager: SettingsManager):
        super().__init__()
        # validator.validate(repository, DataRepository)
        self.__repository = repository
        self.__settings_manager = settings_manager

    def __create_nomenclature_groups(self):
        list = [NomenclatureGroupModel.default_group_cold(), NomenclatureGroupModel.default_group_source() ]
        self.__repository.data[DataRepository.group_key()] = list

    def __create_measurement_units(self):
        current_path_info = os.path.split(__file__)
        current_path = current_path_info[0]
        full_name = f"{current_path}{os.sep}{"resources/measurement_units.json"}"
        with open(full_name) as stream:
            data = json.load(stream)
        units = []
        for k in data.keys():
            base = None
            for unit in units:
                if unit.name == data[k].base:
                    base = unit
                    break
            item = MeasurementUnitModel(k, data[k].unit, base)
            units.append(item)
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
        current_path_info = os.path.split(__file__)
        current_path = current_path_info[0]
        full_name = f"{current_path}{os.sep}{"resources/measurements_units.json"}"
        with open(full_name) as stream:
            recipe_text = json.load(stream)
        title_match = re.search(r'# (.+)', recipe_text)
        recipe_title = title_match.group(1).strip() if title_match else "Без названия"
        time_match = re.search(r'Время приготовления: `(\d+ мин)`', recipe_text)
        cooking_time = time_match.group(1).strip() if time_match else "Время не указано"

        # Парсинг ингредиентов (таблица)
        ingredients = []
        ingredient_table_match = re.search(r'\| Ингредиенты\s+\|\s+Граммовка \|(.+?)\|', recipe_text, re.DOTALL)
        if ingredient_table_match:
            rows = ingredient_table_match.group(1).strip().split('\n')
            for row in rows:
                cols = row.split('|')
                if len(cols) == 3:
                    ingredient = cols[1].strip()
                    quantity = cols[2].strip().split()[0]
                    measurement_unit_name = cols[2].strip().split()[1]
                    measurements = self.__repository.data[DataRepository.measurement_unit_key()]
                    measurement_unit = None
                    for unit in measurements:
                        if unit.name == measurement_unit_name:
                            measurement_unit = unit
                            break
                    ingredients.append(Ingridient(ingredient, measurement_unit, quantity))

        steps_match = re.search(r'## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ(.+)', recipe_text, re.DOTALL)
        steps_text = ""
        if steps_match:
            steps_text = steps_match.group(1).strip()
        recipes = [Recipe(recipe_title, ingredients, cooking_time, steps_text)]
        self.__repository.data[DataRepository.recipe_key()] = recipes


    """
    Первый старт
    """
    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurement_units()
        # self.__create_nomenclature()
        # self.__create_recipe()
