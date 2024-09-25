import os
from abc import ABC, abstractmethod
from pathlib import Path

from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.utils.path_utils import PathUtils


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

    def export(self, path, path_utils: PathUtils = PathUtils()):
        ArgumentException.check_arg(path, str)
        ArgumentException.check_arg(path_utils, PathUtils)
        current_path = Path(__file__).resolve()
        parent_path = path_utils.get_parent_directory(current_path, levels_up=3)
        full_name = os.path.join(parent_path, path)
        Path(str(full_name)).parent.mkdir(parents=True, exist_ok=True)
        with open(full_name, "w", encoding='utf-8') as file:
            file.write(self._result)