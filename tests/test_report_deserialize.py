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
        self.full_name = f"{parent_path}{os.sep}{"reports"}{os.sep}"

    def test_json_measurement_unit_deserialize(self):
        """
        Тестирует десериализацию модели MeasurementUnitModel из формата JSON
        Экспортирует загруженные единицы измерения, потом выгружает обратно и сверяет все поля
        :return:
        """
        measurement_unit_key = self.data_repository.measurement_unit_key()
        self.report.create(self.data_repository.data[measurement_unit_key])
        report_name = "report_measurement_unit.json"
        self.report.export(f"reports/{report_name}")
        self.full_name = f"{self.full_name}{report_name}"
        with open(self.full_name) as file:
            result = JsonModelDecoder().decode(file.read())
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(MeasurementUnitModel, x)),
                             dir(MeasurementUnitModel)))
        measurement_units = self.data_repository.data[measurement_unit_key]
        assert len(result) == len(measurement_units)
        passed = 0
        for i in range(len(result)):
            assert isinstance(result[i], MeasurementUnitModel)
            if result[i] == measurement_units[i]:
                passed += 1
                for field in fields:
                    assert getattr(result[i], field) == getattr(measurement_units[i], field)
        assert passed == len(result)

    def test_json_nomenclatures_deserialize(self):
        """
        Тестирует десериализацию модели NomenclatureModel из формата JSON
        Экспортирует загруженные номенклатуры, потом выгружает обратно и сверяет все поля
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        self.report.create(self.data_repository.data[nomenclature_key])
        report_name = "report_nomenclature.json"
        self.report.export(f"reports/{report_name}")
        self.full_name = f"{self.full_name}{report_name}"
        with open(self.full_name) as file:
            result = JsonModelDecoder().decode(file.read())
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(NomenclatureModel, x)),
                             dir(NomenclatureModel)))
        nomenclatures = self.data_repository.data[nomenclature_key]
        assert len(result) == len(nomenclatures)
        passed = 0
        for i in range(len(result)):
            assert isinstance(result[i], NomenclatureModel)
            if result[i] == nomenclatures[i]:
                passed += 1
                for field in fields:
                    assert getattr(result[i], field) == getattr(nomenclatures[i], field)
        assert passed == len(result)

    def test_json_recipe_deserialize(self):
        """
        Тестирует десериализацию модели RecipeModel из формата JSON
        Экспортирует загруженные рецепты, потом выгружает обратно и сверяет все поля
        :return:
        """
        recipe_key = self.data_repository.recipe_key()
        self.report.create(self.data_repository.data[recipe_key])
        report_name = "report_recipe.json"
        self.report.export(f"reports/{report_name}")
        self.full_name = f"{self.full_name}{report_name}"
        with open(self.full_name) as file:
            result = JsonModelDecoder().decode(file.read())
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(RecipeModel, x)),
                             dir(RecipeModel)))
        recipes = self.data_repository.data[recipe_key]
        assert len(result) == len(recipes)
        passed = 0
        for i in range(len(result)):
            assert isinstance(result[i], RecipeModel)
            if result[i] == recipes[i]:
                passed += 1
                for field in fields:
                    assert getattr(result[i], field) == getattr(recipes[i], field)
        assert passed == len(result)

if __name__ == "__main__":
    unittest.main()