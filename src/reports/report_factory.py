from src.abstract.abstract_logic import AbstractLogic
from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.reports.csv_report import CsvReport


class ReportFactory(AbstractLogic):
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    __reports: dict = {}

    def __init__(self):
        super().__init__()
        self.__reports[FormatReporting.CSV] = CsvReport

    def create(self, format: FormatReporting) -> AbstractReport:
        """
        Получить инстанс нужного отчета
        """
        ArgumentException.check_arg(format, FormatReporting)
        if format not in self.__reports.keys():
            # raise operation_exception(f"Указанный вариант формата не реализован!")
            self.set_exception(OperationException(f"Указанный вариант формата не реализован!"))
        report = self.__reports[format]
        return report()
