import re

from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.data.data_repository import DataRepository
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.models.ingridient_model import IngridientModel
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel


class Parser(AbstractLogic):

    def set_exception(self, ex: Exception):
        pass

    @staticmethod
    def parse_header_recipe(text: str) -> tuple[str, str]:
        title_match = re.search(r'# (.+)', text)
        recipe_title = title_match.group(1).strip() if title_match else "Без названия"
        time_match = re.search(r'Время приготовления: `(\d+)` мин', text)
        cooking_time = time_match.group(1).strip() if time_match else "0"
        return recipe_title, cooking_time

    @staticmethod
    def parse_recipe_ingredients_table(text: str, measurements: list[MeasurementUnitModel], repository: DataRepository) -> list[IngridientModel]:
        ArgumentException.check_arg(repository, DataRepository)
        ingredients = []
        nomenclature_group = NomenclatureGroupModel.create("Продукты")
        nomenclatures = repository.data[repository.nomenclature_key()]
        for line in text.split('\n'):
            if '|' in line and 'ингредиенты' not in line.lower() and 'граммовка' not in line.lower() and '-|' not in line:
                current_row = line.lstrip().split('|')[1:][:-1]
                current_row = [i.strip() for i in current_row]
                count_data = current_row[1].split(' ')
                ingredient_name = current_row[0]
                quantity = float(count_data[0])
                measurement_unit_name = count_data[1]
                measurement_unit = None
                for unit in measurements:
                    if unit.name == measurement_unit_name:
                        measurement_unit = unit
                        break
                if measurement_unit is None:
                    raise OperationException(f'Отсутствует единица измерения {measurement_unit_name}')
                nomenclature = None
                found = False
                for nomenclature in nomenclatures:
                    if nomenclature.name == ingredient_name:
                        nomenclature = nomenclature
                        found = True
                        break
                if not found:
                    nomenclature = NomenclatureModel.create(ingredient_name, nomenclature_group, measurement_unit)
                    nomenclatures.append(nomenclature)
                ingredients.append(IngridientModel.create(nomenclature, quantity))
        return ingredients

    @staticmethod
    def parse_steps(text: str) -> list[str]:
        steps_match = re.search(r'## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ(.+)', text, re.DOTALL)
        steps_text = ""
        if steps_match:
            steps_text = steps_match.group(1).strip()
        if "время приготовления" in steps_text.lower():
            return steps_text.split('\n')[1:]
        return steps_text.split('\n')

    @staticmethod
    def parse_recipe_from_md(text: str, measurements: list[MeasurementUnitModel], repository: DataRepository) -> RecipeModel:
        recipe_title, cooking_time = Parser.parse_header_recipe(text)
        ingredients = Parser.parse_recipe_ingredients_table(text, measurements, repository)
        steps_text = Parser.parse_steps(text)
        recipe = RecipeModel.create(recipe_title, ingredients, int(cooking_time), steps_text)
        return recipe

    @staticmethod
    def parse_measurement_units_from_dict(data: dict):
        units = []
        for k in data.keys():
            base = None
            for unit in units:
                if unit.name == data[k]['base']:
                    base = unit
                    break
            measurement_unit = MeasurementUnitModel.create(k, data[k]['unit'], base)
            units.append(measurement_unit)
        return units

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)

