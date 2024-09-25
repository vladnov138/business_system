from src.abstract.abstract_report import AbstractReport
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException


class RtfReport(AbstractReport):
    """
    Отчет формирует набор данных в формате RTF
    """

    def __init__(self):
        super().__init__()
        self.__format = FormatReporting.RTF

    def create(self, data: list):
        ArgumentException.check_arg(data, list)
        if len(data) == 0:
            raise OperationException("Набор данных пуст!")

        first_model = data[0]
        # список полей
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))
        # мета данные и создание таблицы
        self._result += r"{\rtf1\ansi\deff0" + "\n"
        self._result += r"\trowd\trgaph100" + "\n"
        self._result += r"\b "
        for field in fields:
            self._result += r"\cellx1000 " + field + "\n"
        self._result += r"\b0 " + r"\row\n"

        for row in data:
            for field in fields:
                value = getattr(row, field)
                self._result += r"\cellx1000 " + str(value) + "\n"
            self._result += r"\row\n"

        self._result += "}\n"