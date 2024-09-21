import unittest

from src.data.data_repository import DataRepository
from src.services.start_service import StartService


class TestDataRepository(unittest.TestCase):
    def setUp(self):
        self.data_repository = DataRepository()
        self.service = StartService(self.data_repository)
        self.service.create()

    def test_data_nomenclature_group(self):
        group_key = self.data_repository.group_key()
        nomenclature_groups = self.data_repository.data[group_key]


    def test_data_nomenclature(self):
        nomenclature_key = self.data_repository.nomenclature_key()
        nomenclatures = self.data_repository.data[nomenclature_key]

    def test_data_measurement_units(self):
        measurement_unit_key = self.data_repository.measurement_unit_key()
        measurement_units = self.data_repository.data[measurement_unit_key]

    def test_data_recipes(self):
        recipe_key = self.data_repository.recipe_key()
        recipes = self.data_repository.data[recipe_key]
