import re

from src.abstract.abstract_logic import AbstractLogic
from src.models.ingridient_model import IngridientModel
from src.models.measurement_unit_model import MeasurementUnitModel
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
    def parse_recipe_ingredients_table(text: str, measurements: list[MeasurementUnitModel]) -> list[IngridientModel]:
        ingredients = []
        ingredient_table_match = re.search(r'\| Ингредиенты\s+\|\s+Граммовка \|(.+?)\|', text, re.DOTALL)
        if ingredient_table_match:
            rows = ingredient_table_match.group(1).strip().split('\n')
            for row in rows:
                cols = row.split('|')
                if len(cols) == 3:
                    ingredient = cols[1].strip()
                    quantity = cols[2].strip().split()[0]
                    measurement_unit_name = cols[2].strip().split()[1]
                    measurement_unit = None
                    for unit in measurements:
                        if unit.name == measurement_unit_name:
                            measurement_unit = unit
                            break
                    ingredients.append(IngridientModel(ingredient, measurement_unit, quantity))
        return ingredients

    @staticmethod
    def parse_steps(text: str) -> str:
        steps_match = re.search(r'## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ(.+)', text, re.DOTALL)
        steps_text = ""
        if steps_match:
            steps_text = steps_match.group(1).strip()
        return steps_text

    @staticmethod
    def parse_recipe_from_md(text: str, measurements: list[MeasurementUnitModel]):
        recipe_title, cooking_time = Parser.parse_header_recipe(text)
        ingredients = Parser.parse_recipe_ingredients_table(text, measurements)
        steps_text = Parser.parse_steps(text)
        recipe = RecipeModel(recipe_title, ingredients, int(cooking_time), steps_text)
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
            measurement_unit = MeasurementUnitModel(k, data[k]['unit'], base)
            units.append(measurement_unit)
        return units
