from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException


class CsvReport(AbstractReport):
    """
    Отчет формирует набор данных в формате CSV
    """

    def __init__(self):
        super().__init__()
        self.__format = FormatReporting.CSV

    def create(self, data: list):
        ArgumentException.check_arg(data, list)
        if len(data) == 0:
            raise OperationException("Набор данных пуст!")

        first_model = data[0]
        # список полей
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        for field in fields:
            self._result += f"{field};"
        self._result += "\n"

        for row in data:
            for field in fields:
                value = getattr(row, field)
                self._result += f"{value};"
            self._result += "\n"
