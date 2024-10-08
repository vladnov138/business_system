import unittest

from PyRTF.Elements import Document

from src.abstract.format_reporting import FormatReporting
from src.data.data_repository import DataRepository
from src.reports.csv_report import CsvReport
from src.reports.json_report import JsonReport
from src.reports.md_report import MdReport
from src.reports.report_factory import ReportFactory
from src.reports.rtf_report import RtfReport
from src.reports.xml_report import XmlReport
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestReporting(unittest.TestCase):
    """
    Набор тестов для проверки работы формирования отчетов
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

    def test_csv_report_create_measurement_unit(self):
        """
        Проверка работы отчета CSV на примере создания единицы измерения
        :return:
        """
        report = CsvReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        report.export("reports/report_measurement_unit.csv")
        assert report.result != ""

    def test_csv_report_create_nomenclature(self):
        """
        Проверка работы отчета CSV на примере создания номенклатуры
        :return:
        """
        report = CsvReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        report.export("reports/report_nomenclature.csv")
        assert report.result != ""

    def test_report_factory_create(self):
        """
        Проверка работы фабрики отчетов
        :return:
        """
        report = ReportFactory(self.settings).create(FormatReporting.CSV)
        assert report is not None
        assert isinstance(report, CsvReport)

    def test_md_report_create_measurement_unit(self):
        """
        Проверка работы отчета MarkDown на примере создания единицы измерения
        :return:
        """
        report = MdReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        report.export("reports/report_measurement_unit.md")
        assert report.result != ""

    def test_md_report_create_nomenclature(self):
        """
        Проверка работы отчета MarkDown на примере создания номенклатуры
        :return:
        """
        report = MdReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        report.export("reports/report_nomenclature.md")
        assert report.result != ""

    def test_json_report_create_measurement_unit(self):
        """
        Проверка работы отчета JSON на примере создания единицы измерения
        :return:
        """
        report = JsonReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        report.export("reports/report_measurement_unit.json")
        assert report.result != ""

    def test_json_report_create_nomenclature(self):
        """
        Проверка работы отчета JSON на примере создания номенклатуры
        :return:
        """
        report = JsonReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        report.export("reports/report_nomenclature.json")
        assert report.result != ""

    def test_xml_report_create_measurement_unit(self):
        """
        Проверка работы отчета XML на примере создания единицы измерения
        :return:
        """
        report = XmlReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        report.export("reports/report_measurement_unit.xml")
        assert report.result != ""

    def test_xml_report_create_nomenclature(self):
        """
        Проверка работы отчета XML на примере создания номенклатуры
        :return:
        """
        report = XmlReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        report.export("reports/report_nomenclature.xml")
        assert report.result != ""

    def test_rtf_report_create_measurement_unit(self):
        """
        Проверка работы отчета RTF на примере создания единицы измерения
        :return:
        """
        report = RtfReport()
        report.create(self.repository.data[self.repository.measurement_unit_key()])
        report.export("reports/report_measurement_unit.rtf")
        assert report.result != ""
        assert isinstance(report.document, Document)

    def test_rtf_report_create_nomenclature(self):
        """
        Проверка работы отчета RTF на примере создания номенклатуры
        :return:
        """
        report = RtfReport()
        report.create(self.repository.data[self.repository.nomenclature_key()])
        report.export("reports/report_nomenclature.rtf")
        assert report.result != ""
        assert isinstance(report.document, Document)

if __name__ == "__main__":
    unittest.main()