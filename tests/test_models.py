"""
Набор тестов для проверки работы моделей
"""
import unittest
from datetime import datetime

from src.abstract.transaction_type import TransactionType
from src.exceptions.argument_exception import ArgumentException
from src.models.ingridient_model import IngridientModel
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.organization_model import OrganizationModel
from src.models.recipe_model import RecipeModel
from src.models.warehouse_model import WarehouseModel
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.services.settings_manager import SettingsManager


class TestModels(unittest.TestCase):
    """
    Тестирует модели
    """

    def test_nomenclature_group_model_comparing_by_uid_returns_true(self):
        """
        Тестирует сравнение классов NomenclatureGroupModel по уникальному коду
        Сравнивает экземпляры класса
        Результатом сравнения должен быть True (не равны)
        """
        item1 = NomenclatureGroupModel.create("item1")
        item2 = NomenclatureGroupModel.create("item1")
        assert item1 != item2

    def test_nomenclature_group_model_getters(self):
        """
        Тестирует геттеры класса NomenclatureGroupModel
        Сравнивает имя
        Результатом сравнения должен быть True
        """
        group_name = "group"
        group = NomenclatureGroupModel.create(group_name)
        assert group.name == group_name

    def test_measurement_unit_model_comparing_returns_true(self):
        """
        Тестирует сравнение класса MeasurementUnitModel по наименованию
        Сравнивает экземпляры класса
        Результатом сравнения должен быть True
        """
        unit_name = "грамм"
        g1 = MeasurementUnitModel.create(unit_name, 1)
        g2 = MeasurementUnitModel.create(unit_name, 1000)
        assert g1 == g2

    def test_measurement_unit_model_getters(self):
        """
        Тестирует геттеры класса MeasurementUnitModel
        Сравнивает имя класса и единицы измерения
        Результатом сравнения является True
        """
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel.create(unit_name, unit)
        assert g.unit == unit
        assert g.name == unit_name

    def test_measurement_unit_setters(self):
        """
        Тестирует сеттеры класса MeasurementUnitModel
        Устанавливает значения свойствам unit и name
        Результатом сравнений является True
        """
        unit_name = "грамм"
        unit = 1
        g = MeasurementUnitModel.create("1", 123)
        g.unit = unit
        g.name = unit_name
        assert g.unit == unit
        assert g.name == unit_name

    def test_measurement_base_unit_model(self):
        """
        Тестирует ссылку на базовую единицу измерения класса MeasurementUnitModel
        Создает 3 экземпляра и сравнивает ссылку на базовую единицу измерения с уже созданным
        Результатом сравнения является True
        """
        base_unit_name = "грамм"
        unit_name = "килограмм"
        big_unit_name = "тонна"

        g_unit = MeasurementUnitModel.create(base_unit_name, 1)
        kg_unit = MeasurementUnitModel.create(unit_name, 1000, g_unit)
        t_unit = MeasurementUnitModel.create(big_unit_name, 1000, kg_unit)

        kg_base_unit = kg_unit.base_measure_unit
        t_base_unit = t_unit.base_measure_unit
        assert kg_base_unit == g_unit
        assert t_base_unit == kg_unit

    def test_measurement_unit_exceptions(self):
        """
        Сравнивает проверку типов у класса MeasurementUnitModel
        Создает экземпляр с неправильным типом параметра имени единицы измерения
        Результатом сравнение является получение ArgumentException
        """
        wrong_unit_name = 42
        unit = 1
        with self.assertRaises(ArgumentException):
            MeasurementUnitModel.create(wrong_unit_name, unit)

    def test_nomenclature_model(self):
        """
        Тестирует геттеры класса NomenclatureModel и их классификацию по группам
        Создает два экземпляра sausage и cooker и сравнивает их группу и единицу измерения
        Результатом сравнения является True
        """
        g_unit = MeasurementUnitModel.create("грамм", 1)
        kg_unit = MeasurementUnitModel.create("килограмм", 1000, g_unit)
        ingridients = NomenclatureGroupModel.create("Ингридиенты")
        equipments = NomenclatureGroupModel.create("Оборудование")

        sausage = NomenclatureModel.create("Колбаса", ingridients, kg_unit)
        cooker = NomenclatureModel.create("Плита", equipments, kg_unit)

        assert sausage.nomenclature_group == ingridients
        assert sausage.measurement_unit == kg_unit
        assert cooker.nomenclature_group == equipments
        assert cooker.measurement_unit == kg_unit

    def test_organization_model_converting(self):
        """
        Тестирует геттеры класса OrganizationModel и конвертацию из класса Settings
        Сравнивает геттеры класса OrganizationModel с геттерами класса Settings
        Результатом сравнения является True
        """
        settings_manager = SettingsManager()
        file_path = "resources/test_settings.json"
        settings_manager.open(file_path)
        settings_manager.convert()
        settings = settings_manager.settings

        org = OrganizationModel.create(settings)

        assert org.name == settings.organization_name
        assert org.inn == settings.inn
        assert org.account == settings.account
        assert org.bik == settings.bik
        assert org.business_type == settings.business_type

    def test_ingridient_model(self):
        """
        Тестирует создание модели IngridientModel
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Ингридиенты")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        ingridient = IngridientModel.create(nomenclature, 2)
        assert ingridient.nomenclature.name == "Молоко"
        assert ingridient.nomenclature.measurement_unit == ml
        assert ingridient.amount == 2


    def test_recipe_model(self):
        """
        Тестирует создание модели RecipeModel
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Ингридиенты")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        ingridient = IngridientModel.create(nomenclature, 2)
        recipe = RecipeModel.create("Молоко", [ingridient], 10, ["description"])
        assert recipe.name == "Молоко"
        assert len(recipe.ingridients) == 1
        assert recipe.ingridients[0] == ingridient


    def test_recipe_setters(self):
        """
        Проверяет сеттеры модели RecipeModel
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Ингридиенты")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        ingridient = IngridientModel.create(nomenclature, 2)
        recipe = RecipeModel.create("Молоко", [ingridient], 10, ["description"])
        recipe.name = "Молоко2"
        recipe.ingridients = [ingridient]
        recipe.time = 20
        recipe.description = ["description2"]
        assert recipe.name == "Молоко2"
        assert len(recipe.ingridients) == 1
        assert recipe.ingridients[0] == ingridient
        assert recipe.time == 20
        assert recipe.description[0] == "description2"


    def test_ingridient_model_setters_exceptions(self):
        """
        Проверяет исключения при неправильных типах данных
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Ингридиенты")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        ingridient = IngridientModel.create(nomenclature, 2)
        with self.assertRaises(ArgumentException):
            ingridient.name = 123
        with self.assertRaises(ArgumentException):
            ingridient.nomenclature.measurement_unit = "мл"
        with self.assertRaises(ArgumentException):
            ingridient.amount = 0


    def test_recipe_model_setters_exceptions(self):
        """
        Проверяет исключения при неправильных типах данных
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Ингридиенты")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        ingridient = IngridientModel.create(nomenclature, 2)
        recipe = RecipeModel.create("Молоко", [ingridient], 10, ["description"])
        with self.assertRaises(ArgumentException):
            recipe.name = 123
        with self.assertRaises(ArgumentException):
            recipe.ingridients = ["123"]
        with self.assertRaises(ArgumentException):
            recipe.cooking_time_minutes = -10
        with self.assertRaises(ArgumentException):
            recipe.description = 123

    def test_warehouse_model(self):
        """
        Тестирует создание модели WarehouseModel
        :return:
        """
        warehouse = WarehouseModel.create("Магазин", "Россия, Московская область, г. Москва, ул. Профсоюзная, д. 16")
        assert warehouse.name == "Магазин"
        assert warehouse.address == "Россия, Московская область, г. Москва, ул. Профсоюзная, д. 16"

    def test_warehouse_transaction_model(self):
        """
        Тестирует создание модели WarehouseTransactionModel
        :return:
        """
        ml = MeasurementUnitModel.create("мл", 1)
        nomenclature_group = NomenclatureGroupModel.create("Сырьё")
        warehouse = WarehouseModel.create("Магазин", "Россия, Московская область, г. Москва, ул. Профсоюзная, д. 16")
        nomenclature = NomenclatureModel.create("Молоко", nomenclature_group, ml)
        dt = datetime.now()
        transaction = WarehouseTransactionModel.create("Молоко", warehouse, nomenclature, 10, ml, TransactionType.INCOME, dt)
        assert transaction.name == "Молоко"
        assert transaction.warehouse == warehouse
        assert transaction.nomenclature == nomenclature
        assert transaction.amount == 10
        assert transaction.measurement_unit == ml
        assert transaction.transaction_type == TransactionType.INCOME
        assert transaction.period == dt

if __name__ == "__main__":
    unittest.main()