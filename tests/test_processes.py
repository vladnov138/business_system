import time
import unittest
from asyncio.subprocess import Process
from datetime import datetime, timedelta

from matplotlib import pyplot as plt

from main import repository
from src.abstract.process_type import ProcessType
from src.abstract.transaction_type import TransactionType
from src.data.data_repository import DataRepository
from src.logics.date_block_observer import DateBlockUpdator
from src.processes.process_factory import ProcessFactory
from src.processes.warehouse_turnover_process import WarehouseTurnoverProcess
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

    def test_dateblock_process(self):
        """
        Проверка работы процесса подсчета обороты с учетом даты блокировки
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
        test_transactions = [transaction1, transaction2]
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        transactions += test_transactions
        turnover_key = self.repository.turnovers_key()
        process = ProcessFactory().create(ProcessType.DATEBLOCK,
                                          dateblock=self.settings.date_block,
                                          turnovers=self.repository.data[turnover_key])
        turnovers1 = process.execute(transactions)

        self.settings.date_block = datetime.now()
        process = ProcessFactory().create(ProcessType.DATEBLOCK,
                                          dateblock=self.settings.date_block,
                                          turnovers=turnovers1)
        turnovers2 = process.execute(transactions)
        assert len(turnovers1) == len(turnovers2)
        assert turnovers1[0].turnover == turnovers2[0].turnover

    def test_dateblock_turnovers_speed(self):
        """
        Нагрузочный тест подсчета оборота при разных датах блокировки
        :return: график в /demo
        """
        # Подготовка
        count = 1000
        start_date = datetime(2000, 1, 1)
        end_date = start_date + timedelta(days=count)
        warehouse_key = self.repository.warehouse_key()
        warehouse = self.repository.data[warehouse_key][0]
        nomenclature_key = self.repository.nomenclature_key()
        nomenclature = self.repository.data[nomenclature_key][0]
        measurement_key = self.repository.measurement_unit_key()
        measurement_unit = self.repository.data[measurement_key][0]
        transaction_key = self.repository.warehouse_transaction_key()
        turnover_key = self.repository.turnovers_key()

        transactions = []
        for i in range(count):
            transaction_type = TransactionType.INCOME if i % 2 == 0 else TransactionType.EXPENSE
            transaction = WarehouseTransactionModel.create(
                f"Transaction {i}", warehouse, nomenclature, i, measurement_unit, transaction_type,
                start_date + timedelta(days=i))
            transactions.append(transaction)

        self.repository.data[transaction_key] = transactions
        self.repository.data[turnover_key] = []

        # даты блокировки
        dates = [start_date + (end_date - start_date) * i / 9 for i in range(10)]
        dateblock_ = datetime(1900, 1, 1)
        process_factory = ProcessFactory()
        dateblock_observer = DateBlockUpdator(dateblock_, repository, process_factory, ProcessType.DATEBLOCK)

        # запускаем обход
        for dateblock in dates:
            dates_x = []
            result_time = []
            self.settings.date_block = dateblock
            dateblock_observer.update(dateblock)
            turnovers = self.repository.data[turnover_key]
            # Замер времени обработки транзакций
            for x in range(10, len(transactions), 10):
                # Запись времени начала
                start_time = time.time()

                process = process_factory.create(ProcessType.DATEBLOCK, turnovers=turnovers, dateblock=dateblock)
                result = process.execute(transactions[:x])

                # Запись времени окончания
                end_time = time.time()
                execution_time = end_time - start_time
                result_time.append(execution_time)
                dates_x.append(x)

            plt.plot(dates_x, result_time, label=f"{dateblock.date()}")
        plt.title(f"test speed on date:{start_date.date()}-{end_date.date()}")
        plt.xlabel(f"count_transaction ")
        plt.ylabel(f"time in seconds")
        plt.legend()
        # plt.savefig("../demo/test_speed.png")
        plt.close()


if __name__ == '__main__':
    unittest.main()
