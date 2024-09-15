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

"""
Тестирует модели
"""
class TestModels(unittest.TestCase):
    """
    Тестирует сравнение классов NomenclatureGroupModel по уникальному коду
    Сравнивает экземпляры класса
    Результатом сравнения должен быть True (не равны)
    """
    def test_nomenclature_group_model_comparing_by_uid_returns_true(self):
        item1 = NomenclatureGroupModel("item1")
        item2 = NomenclatureGroupModel("item1")
        assert item1 != item2

    """
    Тестирует геттеры класса NomenclatureGroupModel
    Сравнивает имя
    Результатом сравнения должен быть True
    """
    def test_nomenclature_group_model_getters(self):
        group_name = "group"
        group = NomenclatureGroupModel(group_name)
        assert group.name == group_name

    """
    Тестирует сравнение класса MeasurementUnitModel по наименованию
    Сравнивает экземпляры класса
    Результатом сравнения должен быть True
    """
    def test_measurement_unit_model_comparing_returns_true(self):
        unit_name = "грамм"
        g1 = MeasurementUnitModel(unit_name, 1)
        g2 = MeasurementUnitModel(unit_name, 1000)
        assert g1 == g2

    """
    Тестирует геттеры класса MeasurementUnitModel
    Сравнивает имя класса и единицы измерения
    Результатом сравнения является True
    """
    def test_measurement_unit_model_getters(self):
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel(unit_name, unit)
        assert g.unit == unit
        assert g.name == unit_name

    """
    Тестирует сеттеры класса MeasurementUnitModel
    Устанавливает значения свойствам unit и name
    Результатом сравнений является True
    """
    def test_measurement_unit_setters(self):
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel("1", 123)
        g.unit = unit
        g.name = unit_name
        assert g.unit == unit
        assert g.name == unit_name

    """
    Тестирует ссылку на базовую единицу измерения класса MeasurementUnitModel
    Создает 3 экземпляра и сравнивает ссылку на базовую единицу измерения с уже созданным
    Результатом сравнения является True
    """
    def test_measurement_base_unit_model(self):
        base_unit_name = "грамм"
        unit_name = "килограмм"
        big_unit_name = "тонна"

        g_unit = MeasurementUnitModel(base_unit_name, 1)
        kg_unit = MeasurementUnitModel(unit_name, 1000, g_unit)
        t_unit = MeasurementUnitModel(big_unit_name, 1000, kg_unit)

        kg_base_unit = kg_unit.base_measure_unit
        t_base_unit = t_unit.base_measure_unit
        assert kg_base_unit == g_unit
        assert t_base_unit == kg_unit

    """
    Сравнивает проверку типов у класса MeasurementUnitModel
    Создает экземпляр с неправильным типом параметра имени единицы измерения
    Результатом сравнение является получение ArgumentException
    """
    def test_measurement_unit_exceptions(self):
        wrong_unit_name = 42
        unit = 1
        with self.assertRaises(ArgumentException):
            MeasurementUnitModel(wrong_unit_name, unit)

    """
    Тестирует геттеры класса NomenclatureModel и их классификацию по группам
    Создает два экземпляра sausage и cooker и сравнивает их группу и единицу измерения
    Результатом сравнения является True
    """
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

    """
    Тестирует геттеры класса OrganizationModel и конвертацию из класса Settings
    Сравнивает геттеры класса OrganizationModel с геттерами класса Settings
    Результатом сравнения является True
    """
    def test_organization_model_converting(self):
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

    """
    Тестирует геттеры у класса StorageModel
    Сравнивает имя
    Результатом сравнения является True
    """
    def test_storage_model_getters(self):
        storage_name = "IdkWhatThis"
        storage = StorageModel(storage_name)
        assert storage.name == storage_name