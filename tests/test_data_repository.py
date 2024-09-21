import unittest

from src.data.data_repository import DataRepository
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.services.start_service import StartService
from src.settings.settings_manager import SettingsManager


class TestDataRepository(unittest.TestCase):
    """
    Тестирует репозиторий
    """

    def setUp(self):
        """
        Настройки перед каждым тестом
        :return:
        """
        self.data_repository = DataRepository()
        settings_manager = SettingsManager()
        settings_manager.open("resources/settings.json")
        settings_manager.convert()
        settings = settings_manager.settings
        self.service = StartService(self.data_repository, settings)
        self.service.create()

    def test_data_nomenclature_group(self):
        """
        Тестирует, что в репозитории есть 2 группы номенклатуры
        :return:
        """
        group_key = self.data_repository.group_key()
        nomenclature_groups = self.data_repository.data[group_key]
        assert len(nomenclature_groups) == 2
        for group in nomenclature_groups:
            assert isinstance(group, NomenclatureGroupModel)


    def test_data_nomenclature(self):
        """
        Тестирует, что в репозитории есть 2 номенклатуры
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        assert len(nomenclatures) == 2
        for nomenclature in nomenclatures:
            assert isinstance(nomenclature, NomenclatureModel)

    def test_data_measurement_units(self):
        """
        Тестирует, что в репозитории есть 6 единиц измерения
        :return:
        """
        measurement_unit_key = self.data_repository.measurement_unit_key()
        measurement_units = self.data_repository.data[measurement_unit_key]
        assert len(measurement_units) == 6
        for measurement_unit in measurement_units:
            assert isinstance(measurement_unit, MeasurementUnitModel)

    def test_data_recipes(self):
        """
        Тестирует, что в репозитории есть 2 рецепты
        :return:
        """
        recipe_key = self.data_repository.recipe_key()
        recipes = self.data_repository.data[recipe_key]
        assert len(recipes) == 2
        for recipe in recipes:
            assert isinstance(recipe, RecipeModel)
