import json

from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.reports.report_factory import ReportFactory
from src.services.settings_manager import SettingsManager


class ReportService:
    def __init__(self):
        self.manager = SettingsManager()

    def get_report(self, data, format: FormatReporting) -> AbstractReport:
        report = ReportFactory(self.manager.settings).create(format)
        report.create(data)
        return report

    def prepare_report(self, data):
        report_format = FormatReporting(self.manager.settings.report_format)
        report = ReportFactory(self.manager.settings).create(report_format)
        report.create(data)
        return json.loads(report.result)