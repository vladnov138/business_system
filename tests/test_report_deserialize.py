import os
import unittest
from pathlib import Path

from src.data.data_repository import DataRepository
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.reports.json_report import JsonReport
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService
from src.utils.json_model_decoder import JsonModelDecoder
from src.utils.path_utils import PathUtils


class TestReportDeserialize(unittest.TestCase):
    """
    Тестирование десериализации отчетов разных форматов
    """

    def setUp(self):
        """
        Подготовка перед каждым тестом
        :return:
        """
        self.data_repository = DataRepository()
        settings_manager = SettingsManager()
        settings_manager.open("resources/settings.json")
        settings_manager.convert()
        settings = settings_manager.settings
        self.service = StartService(self.data_repository, settings)
        self.service.create()
        self.report = JsonReport()
        parent_path = PathUtils().get_parent_directory(Path(__file__).resolve(), levels_up=2)
        self.full_name = f"{parent_path}{os.sep}reports{os.sep}"

    def get_fields(self, model_class):
        """
        Получает поля класса модели для проверки
        :return:
        """
        return list(filter(lambda x: not x.startswith("_") and not callable(getattr(model_class, x)),
                           dir(model_class)))

    def deserialize_json(self, data, report_name):
        """
        Экспортирует данные, десериализует и возвращает результат
        :return:
        """
        self.report.create(data)
        full_name = f"{self.full_name}{report_name}"
        self.report.export(f"/reports/{report_name}")
        with open(full_name) as file:
            result = JsonModelDecoder().decode(file.read())
        return result

    def test_json_measurement_unit_deserialize(self):
        """
        Тестирует десериализацию модели MeasurementUnitModel из формата JSON
        Экспортирует загруженные единицы измерения и сверяет кол-во экземпляров
        :return:
        """
        measurement_unit_key = self.data_repository.measurement_unit_key()
        measurement_units = self.data_repository.data[measurement_unit_key]
        result = self.deserialize_json(measurement_units, "report_measurement_unit.json")
        assert len(result) == len(measurement_units)

    def test_measurement_unit_instance(self):
        """
        Тестирует десериализацию модели MeasurementUnitModel из формата JSON
        Экспортирует загруженные единицы измерения и проверяет, что все сущности это MeasurementUnitModel
        :return:
        """
        measurement_unit_key = self.data_repository.measurement_unit_key()
        measurement_units = self.data_repository.data[measurement_unit_key]
        result = self.deserialize_json(measurement_units, "report_measurement_unit.json")
        for item in result:
            assert isinstance(item, MeasurementUnitModel)

    def test_measurement_unit_fields(self):
        """
        Тестирует десериализацию модели MeasurementUnitModel из формата JSON
        Экспортирует загруженные единицы измерения и сравнивает все поля
        :return:
        """
        measurement_unit_key = self.data_repository.measurement_unit_key()
        measurement_units = self.data_repository.data[measurement_unit_key]
        result = self.deserialize_json(measurement_units, "report_measurement_unit.json")
        fields = self.get_fields(MeasurementUnitModel)
        for i in range(len(result)):
            assert result[i] == measurement_units[i]
            for field in fields:
                assert getattr(result[i], field) == getattr(measurement_units[i], field)

    def test_json_nomenclature_deserialize(self):
        """
        Тестирует десериализацию модели NomenclatureModel из формата JSON
        Экспортирует загруженные единицы измерения и сверяет кол-во экземпляров
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        result = self.deserialize_json(nomenclatures, "report_nomenclature.json")
        assert len(result) == len(nomenclatures)

    def test_nomenclature_instance(self):
        """
        Тестирует десериализацию модели NomenclatureModel из формата JSON
        Экспортирует загруженные единицы измерения и проверяет, что все сущности это NomenclatureModel
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        result = self.deserialize_json(nomenclatures, "report_nomenclature.json")
        for item in result:
            assert isinstance(item, NomenclatureModel)

    def test_nomenclature_fields(self):
        """
        Тестирует десериализацию модели NomenclatureModel из формата JSON
        Экспортирует загруженные единицы измерения и сравнивает все поля
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        result = self.deserialize_json(nomenclatures, "report_measurement_unit.json")
        fields = self.get_fields(NomenclatureModel)
        for i in range(len(result)):
            assert result[i] == nomenclatures[i]
            for field in fields:
                assert getattr(result[i], field) == getattr(nomenclatures[i], field)

    def test_json_recipe_deserialize(self):
        """
        Тестирует десериализацию модели RecipeModel из формата JSON
        Экспортирует загруженные единицы измерения и сверяет кол-во экземпляров
        :return:
        """
        recipe_key = self.data_repository.recipe_key()
        recipes = self.data_repository.data[recipe_key]
        result = self.deserialize_json(recipes, "report_recipe.json")
        assert len(result) == len(recipes)

    def test_recipe_instance(self):
        """
        Тестирует десериализацию модели RecipeModel из формата JSON
        Экспортирует загруженные единицы измерения и проверяет, что все сущности это RecipeModel
        :return:
        """
        recipe_key = self.data_repository.recipe_key()
        recipes = self.data_repository.data[recipe_key]
        result = self.deserialize_json(recipes, "report_recipe.json")
        for item in result:
            assert isinstance(item, RecipeModel)

    def test_recipe_fields(self):
        """
        Тестирует десериализацию модели RecipeModel из формата JSON
        Экспортирует загруженные единицы измерения и сравнивает все поля
        :return:
        """
        recipe_key = self.data_repository.recipe_key()
        recipes = self.data_repository.data[recipe_key]
        result = self.deserialize_json(recipes, "report_recipe.json")
        fields = self.get_fields(RecipeModel)
        for i in range(len(result)):
            assert result[i] == recipes[i]
            for field in fields:
                assert getattr(result[i], field) == getattr(recipes[i], field)

if __name__ == "__main__":
    unittest.main()