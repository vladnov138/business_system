import unittest
from datetime import datetime

from src.abstract.process_type import ProcessType
from src.abstract.transaction_type import TransactionType
from src.data.data_repository import DataRepository
from src.logics.process_factory import ProcessFactory
from src.logics.warehouse_turnover_process import WarehouseTurnoverProcess
from src.models.warehouse_model import WarehouseModel
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestProcesses(unittest.TestCase):
    def setUp(self):
        """
        Начальная настройка перед каждым тестом
        :return:
        """
        settings_manager = SettingsManager()
        settings_manager.open("resources/settings.json")
        settings_manager.convert()
        self.settings = settings_manager.settings
        self.repository = DataRepository()
        self.start = StartService(self.repository, self.settings)
        self.start.create()

    def test_turnover_only_income_process(self):
        """
        Тестирует расчет оборота только по приходу
        Создает 2 транзакции по одной номенклатуре и складу и сравнивает оборот с ответом
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        nomenclature = self.repository.data[self.repository.nomenclature_key()][0]
        measurement_unit = self.repository.data[self.repository.measurement_unit_key()][0]
        transaction1 = WarehouseTransactionModel.create(
            "test_transaction1", warehouse, nomenclature, 10, measurement_unit, TransactionType.INCOME, datetime.now()
        )
        transaction2 = WarehouseTransactionModel.create(
            "test_transaction2", warehouse, nomenclature, 20, measurement_unit, TransactionType.INCOME, datetime.now()
        )
        transactions = [transaction1, transaction2]
        process = WarehouseTurnoverProcess()
        turns = process.execute(transactions)
        assert len(turns) == 1
        assert turns[0].turnover == 30

    def test_turnover_only_expense_process(self):
        """
        Тестирует расчет оборота только по расходу
        Создает 2 транзакции по одной номенклатуре и складу и сравнивает оборот с ответом
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        nomenclature = self.repository.data[self.repository.nomenclature_key()][0]
        measurement_unit = self.repository.data[self.repository.measurement_unit_key()][0]
        transaction1 = WarehouseTransactionModel.create(
            "test_transaction1", warehouse, nomenclature, 10, measurement_unit, TransactionType.EXPENSE, datetime.now()
        )
        transaction2 = WarehouseTransactionModel.create(
            "test_transaction2", warehouse, nomenclature, 20, measurement_unit, TransactionType.EXPENSE, datetime.now()
        )
        transactions = [transaction1, transaction2]
        process = WarehouseTurnoverProcess()
        turns = process.execute(transactions)
        assert len(turns) == 1
        assert turns[0].turnover == -30

    def test_turnover_both_process(self):
        """
        Тестирует расчет оборота по приходу и расходу
        Создает 2 транзакции по одной номенклатуре и складу и сравнивает оборот с ответом
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        nomenclature = self.repository.data[self.repository.nomenclature_key()][0]
        measurement_unit = self.repository.data[self.repository.measurement_unit_key()][0]
        transaction1 = WarehouseTransactionModel.create(
            "test_transaction1", warehouse, nomenclature, 20, measurement_unit, TransactionType.INCOME, datetime.now()
        )
        transaction2 = WarehouseTransactionModel.create(
            "test_transaction2", warehouse, nomenclature, 10, measurement_unit, TransactionType.EXPENSE, datetime.now()
        )
        transactions = [transaction1, transaction2]
        process = WarehouseTurnoverProcess()
        turns = process.execute(transactions)
        assert len(turns) == 1
        assert turns[0].turnover == 10

    def test_process_factory(self):
        """
        Проверка работы фабрики процессов
        :return:
        """
        process = ProcessFactory().create(ProcessType.TURNOVER)
        assert process is not None
        assert isinstance(process, WarehouseTurnoverProcess)


if __name__ == '__main__':
    unittest.main()
