"""
Набор тестов для проверки работы моделей
"""
import unittest

from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.organization_model import OrganizationModel
from src.models.storage_model import StorageModel
from src.settings.settings_manager import SettingsManager


class TestModels(unittest.TestCase):
    """
    Проверить вариант сравнения (по коду)
    """
    def test_nomenclature_group_model_comparing(self):
        item1 = NomenclatureGroupModel("item1")
        item2 = NomenclatureGroupModel("item1")
        assert item1 != item2

    def test_nomenclature_group_model(self):
        group_name = "group"
        group = NomenclatureGroupModel(group_name)
        assert group.name == group_name

    """
    Проверить вариант сравнения (по наименованию)
    """
    def test_measurement_unit_model_comparing(self):
        unit_name = "грамм"
        g1 = MeasurementUnitModel(unit_name, 1)
        g2 = MeasurementUnitModel(unit_name, 1000)
        assert g1 == g2

    def test_measurement_unit_model(self):
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel(unit_name, unit)
        assert g.unit == unit
        assert g.name == unit_name

    def test_measurement_unit_setters(self):
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel("1", 123)
        g.unit = unit
        g.name = unit_name
        assert g.unit == unit
        assert g.name == unit_name

    def test_measurement_base_unit_model(self):
        base_unit_name = "грамм"
        unit_name = "килограмм"
        big_unit_name = "тонна"
        g_unit = MeasurementUnitModel(base_unit_name, 1)
        kg_unit = MeasurementUnitModel(unit_name, 1000, g_unit)
        t_unit = MeasurementUnitModel(big_unit_name, 1000, kg_unit)
        assert kg_unit.base_measure_unit == g_unit
        assert t_unit.base_measure_unit == kg_unit

    def test_measurement_unit_exceptions(self):
        wrong_unit_name = 42
        unit = 1
        with self.assertRaises(ArgumentException) as context:
            MeasurementUnitModel(wrong_unit_name, unit)
        self.assertIn("Argument 'name' must be of type str, not int", str(context.exception))

    def test_nomenclature_model(self):
        g_unit = MeasurementUnitModel("грамм", 1)
        kg_unit = MeasurementUnitModel("килограмм", 1000, g_unit)
        ingridients = NomenclatureGroupModel("Ингридиенты")
        equipments = NomenclatureGroupModel("Оборудование")

        sausage = NomenclatureModel("Колбаса", ingridients, kg_unit)
        cooker = NomenclatureModel("Плита", equipments, kg_unit)
        assert sausage.nomenclature_group == ingridients
        assert sausage.measurement_unit == kg_unit
        assert cooker.nomenclature_group == equipments
        assert cooker.measurement_unit == kg_unit

    def test_nomenclature_setters(self):
        pass

    def test_nomenclature_exceptions(self):
        pass

    def test_nomenclature_setters_exceptions(self):
        pass

    def test_organization_model(self):
        settings_manager = SettingsManager()
        file_path = "../resources/test_settings.json"
        settings_manager.open(file_path)
        settings_manager.convert()
        settings = settings_manager.settings
        org = OrganizationModel(settings)
        assert org.name == settings.organization_name
        assert org.inn == settings.inn
        assert org.account == settings.account
        assert org.bik == settings.bik
        assert org.business_type == settings.business_type

    def test_storage_model(self):
        storage_name = "IdkWhatThis"
        storage = StorageModel(storage_name)
        assert storage.name == storage_name