import unittest

from src.abstract.format_reporting import FormatReporting
from src.data.data_repository import DataRepository
from src.reports.csv_report import CsvReport
from src.reports.json_report import JsonReport
from src.reports.md_report import MdReport
from src.reports.report_factory import ReportFactory
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestReporting(unittest.TestCase):
    """
    Набор тестов для проверки работы формирования отчетов
    """

    def setUp(self):
        settings_manager = SettingsManager()
        settings_manager.open("resources/settings.json")
        settings_manager.convert()
        settings = settings_manager.settings
        self.repository = DataRepository()
        self.start = StartService(self.repository, settings)
        self.start.create()

    def test_csv_report_create_range(self):
        """
        Проверка работы отчета CSV
        """
        report = CsvReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        assert report.result != ""

    def test_csv_report_create_nomenclature(self):
        """
        Проверка работы отчета CSV
        """
        report = CsvReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        assert report.result != ""

    def test_report_factory_create(self):
        report = ReportFactory().create(FormatReporting.CSV)
        assert report is not None
        assert isinstance(report, CsvReport)

    def test_md_report_create_range(self):
        report = MdReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        assert report.result != ""

    def test_md_report_create_nomenclature(self):
        """
        Проверка работы отчета MarkDown
        """
        report = MdReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        assert report.result != ""

    def test_json_report_create_range(self):
        report = JsonReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        assert report.result != ""

    def test_json_report_create_nomenclature(self):
        """
        Проверка работы отчета JSON
        """
        report = JsonReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        assert report.result != ""

if __name__ == "__main__":
    unittest.main()