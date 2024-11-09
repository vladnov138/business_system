import unittest

from src.data.data_repository import DataRepository
from src.models.nomenclature_model import NomenclatureModel
from src.services.filter_service import FilterService
from src.services.nomenclature_service import NomenclatureService
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestNomenclatureService(unittest.TestCase):
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
        filter_service = FilterService()
        self.nomenclature_service = NomenclatureService(self.data_repository, filter_service)

    def test_add_nomenclature(self):
        """
        Тестирует добавление номенклатуры
        :return:
        """
        pass

    def test_get_nomenclature(self):
        """
        Тестирует получение номенклатуры
        :return:
        """
        pass

    def test_update_nomenclature(self):
        """
        Тестирует обновление номенклатуры
        :return:
        """
        pass

    def test_delete_nomenclature(self):
        """
        Тестирует удаление номенклатуры
        :return:
        """
        pass