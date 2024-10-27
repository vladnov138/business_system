from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.reports.report_factory import ReportFactory
from src.services.settings_manager import SettingsManager


class ReportService:
    def get_report(data, format: FormatReporting) -> AbstractReport:
        manager = SettingsManager()
        report = ReportFactory(manager.settings).create(format)
        report.create(data)
        return report