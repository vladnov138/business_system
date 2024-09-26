import os
from abc import ABC, abstractmethod
from pathlib import Path

from src.abstract.abstract_logic import AbstractLogic
from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException
from src.utils.path_utils import PathUtils


class AbstractReport(AbstractLogic):
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

    def export(self, path, path_utils: PathUtils = PathUtils()) -> bool:
        ArgumentException.check_arg(path, str)
        ArgumentException.check_arg(path_utils, PathUtils)
        try:
            current_path_info = os.path.split(__file__)
            current_path = current_path_info[0]
            parent_path = path_utils.get_parent_directory(current_path, levels_up=2)
            full_name = f"{parent_path}{os.sep}{path}"
            Path(str(full_name)).parent.mkdir(parents=True, exist_ok=True)
            with open(full_name, "w", encoding='utf-8') as file:
                file.write(self._result)
            return True
        except Exception as ex:
            self.set_exception(ex)
            return False

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

