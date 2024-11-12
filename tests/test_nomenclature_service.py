import unittest

from src.data.data_repository import DataRepository
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
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
        g_unit = MeasurementUnitModel.create("грамм", 1)
        kg_unit = MeasurementUnitModel.create("килограмм", 1000, g_unit)
        ingridients = NomenclatureGroupModel.create("Ингридиенты")
        sausage = NomenclatureModel.create("Колбаса", ingridients, kg_unit)
        nomenclature_key = self.data_repository.nomenclature_key()
        prev_length = len(self.data_repository.data[nomenclature_key])
        self.nomenclature_service.add_nomenclature(sausage)
        new_length = len(self.data_repository.data[nomenclature_key])
        assert new_length - prev_length == 1

    def test_get_nomenclature(self):
        """
        Тестирует получение номенклатуры
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        nomenclature = nomenclatures[0]
        result = self.nomenclature_service.get_nomenclature(nomenclature.uid)
        assert result == nomenclature

    def test_update_nomenclature(self):
        """
        Тестирует обновление номенклатуры
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        nomenclature = nomenclatures[0]
        new_name = "TestName2"
        nomenclature.name = new_name
        self.nomenclature_service.update_nomenclature(nomenclature)
        result = nomenclatures[0]
        assert result.name == new_name

    def test_delete_nomenclature(self):
        """
        Тестирует удаление номенклатуры
        :return:
        """
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]
        nomenclature = nomenclatures[0]
        prev_length = len(nomenclatures)
        self.nomenclature_service.delete_nomenclature(nomenclature.uid)
        new_length = len(nomenclatures)
        assert prev_length - new_length == 1
        assert nomenclature not in nomenclatures