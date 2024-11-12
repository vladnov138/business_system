from src.abstract.abstract_logic import AbstractLogic
from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.core.event_type import EventType
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.models.settings_model import Settings


class ReportFactory(AbstractLogic):
    __reports: dict = {}
    __settings: Settings = None

    def __init__(self, settings: Settings):
        super().__init__()
        ArgumentException.check_arg(settings, Settings)
        self.__settings = settings
        self.__reports = settings.format_reports

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def create(self, format: FormatReporting) -> AbstractReport:
        """
        Получить инстанс нужного отчета
        """
        ArgumentException.check_arg(format, FormatReporting)
        if format not in self.__reports.keys():
            self.set_exception(OperationException(f"Указанный вариант формата не реализован!"))
        report = self.__reports[format]
        return report()

    def create_default(self):
        return self.create(self.__settings.report_format)

    @property
    def settings(self) -> Settings:
        return self.__settings

    @settings.setter
    def settings(self, value: Settings):
        ArgumentException.check_arg(value, Settings)
        self.__settings = value

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)

