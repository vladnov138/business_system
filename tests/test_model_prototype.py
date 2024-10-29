import unittest

from main import repository
from src.abstract.filter_type import FilterType
from src.data.data_repository import DataRepository
from src.dto.filter_dto import FilterDto
from src.logics.filter_item import FilterItem
from src.logics.model_prototype import ModelPrototype
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestCase(unittest.TestCase):
    """
    Набор тестов для проверки работы прототипа фильтрации
    """

    def setUp(self):
        """
        Начальная настройка перед каждым тестом
        :return:
        """
        settings_manager = SettingsManager()
        settings_manager.open("resources/settings.json")
        settings_manager.convert()
        self.settings = settings_manager.settings
        self.repository = DataRepository()
        self.start = StartService(self.repository, self.settings)
        self.start.create()

    def test_like_name_filter(self):
        """
        Проверка работы фильтрации по вхождению имени
        Фильтрация по вхождению имени букве "ш"
        Результатом сравнения является список из 1 элемента
        :return:
        """
        filter_item = FilterItem.create("name", FilterType.LIKE, "ш")
        key = repository.measurement_unit_key()
        data = repository.data[key]
        model_prototype = ModelPrototype(data)
        result = model_prototype.create(filter_item).data
        assert len(result) == 1

    def test_equal_name_filter(self):
        """
        Проверка работы фильтрации по равенству имени
        Фильтрация по равенству имени букве "г"
        Результатом сравнения является список из 3 элементов (т.к. проверяется вхождение вложенных элементов)
        :return:
        """
        filter_item = FilterItem.create("name", FilterType.EQUAL, "г")
        key = repository.measurement_unit_key()
        data = repository.data[key]
        model_prototype = ModelPrototype(data)
        result = model_prototype.create(filter_item).data
        assert len(result) == 3

    def test_like_id_filter(self):
        """
        Проверка работы фильтрации по вхождению идентификатора
        Берутся первые 2 символа id первого элемента и проверяется его наличие в результате
        Результатом сравнения является вхождение первого элемента в результат
        :return:
        """
        key = repository.measurement_unit_key()
        data = repository.data[key]
        first_item = data[0]
        part_of_id = first_item.uid[:2]
        filter_item = FilterItem.create("uid", FilterType.LIKE, part_of_id)
        model_prototype = ModelPrototype(data)
        result = model_prototype.create(filter_item).data
        assert first_item in result

    def test_equal_id_filter(self):
        """
        Проверка работы фильтрации по вхождению идентификатора
        Берется id первого элемента и проверяется его наличие в результате
        Результатом сравнения является список из первого элемента
        :return:
        """
        key = repository.group_key()
        data = repository.data[key]
        first_item = data[0]
        id = first_item.uid
        filter_item = FilterItem.create("uid", FilterType.EQUAL, id)
        model_prototype = ModelPrototype(data)
        result = model_prototype.create(filter_item).data
        assert len(result) == 1
        assert result[0] == first_item