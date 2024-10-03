import os
import unittest
from pathlib import Path

from src.utils.json_model_decoder import JsonModelDecoder
from src.utils.path_utils import PathUtils


class TestReportDeserialize(unittest.TestCase):
    """
    Тестирование десериализации отчетов разных форматов
    """

    def test_json_measurement_unit_deserialize(self):
        """
        Тестирует десериализацию модели MeasurementUnitModel из формата JSON
        :return:
        """
        parent_path = PathUtils().get_parent_directory(Path(__file__).resolve(), levels_up=2)
        full_name = f"{parent_path}{os.sep}{"reports/report_measurement_unit.json"}"
        with open(full_name) as file:
            result = JsonModelDecoder().raw_decode(file.read())
        assert True

    def test_json_nomenclatures_deserialize(self):
        """
        Тестирует десериализацию модели NomenclatureModel из формата JSON
        :return:
        """
        parent_path = PathUtils().get_parent_directory(Path(__file__).resolve(), levels_up=2)
        full_name = f"{parent_path}{os.sep}{"reports/report_nomenclature.json"}"
        with open(full_name) as file:
            result = JsonModelDecoder().raw_decode(file.read())
        assert True

if __name__ == "__main__":
    unittest.main()