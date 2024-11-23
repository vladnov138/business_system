"""
Репозиторий
"""
from pathlib import Path

from src.exceptions.argument_exception import ArgumentException


class DataRepository:
    __data = {}
    __default_file_name = "exported_data"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataRepository, cls).__new__(cls)
        return cls.instance

    """
    Набор данных
    """
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value: dict):
        ArgumentException.check_arg(value, dict)
        self.__data = value

    """
    Ключ для хранения групп номенклатуры
    """
    @staticmethod
    def group_key() -> str:
        return "group"

    @staticmethod
    def measurement_unit_key() -> str:
        return "measurement_unit"

    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"

    @staticmethod
    def recipe_key() -> str:
        return "recipe"

    @staticmethod
    def warehouse_transaction_key() -> str:
        return "warehouse_transaction"

    @staticmethod
    def warehouse_key() -> str:
        return "warehouse"

    @staticmethod
    def turnovers_key() -> str:
        return "turnovers"

    @staticmethod
    def balance_sheet_key() -> str:
        return "balance_sheet_key"