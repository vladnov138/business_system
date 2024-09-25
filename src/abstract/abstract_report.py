from abc import ABC, abstractmethod

from src.abstract.format_reporting import FormatReporting


class AbstractReport(ABC):
    """
    Абстрактный класс для наследования для отчетов
    """

    _format: FormatReporting = FormatReporting.CSV
    _file_name: str = ""
    _result: str = ""

    @abstractmethod
    def create(self, file_name: str, data):
        """
        Сформировать
        """
        pass

    @property
    def result(self) -> str:
        """
        Результат формирования отчета
        """
        return self._result

    @result.setter
    def result(self, value):
        self._result = value