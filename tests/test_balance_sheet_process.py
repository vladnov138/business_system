import datetime
import os
import unittest

import pandas as pd
from matplotlib import pyplot as plt

from src.abstract.process_type import ProcessType
from src.data.data_repository import DataRepository
from src.processes.process_factory import ProcessFactory
from src.services.settings_manager import SettingsManager
from src.services.start_service import StartService


class TestBalanceSheetProcess(unittest.TestCase):
    """
    Тестирование процесса BalanceSheetProcess
    """

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

    def test_beginning_balance(self):
        """
        Проверяет стартовый баланс на период с 01.01.2021 по 01.01.2025
        Результатом сравнения должен быть 90
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=datetime.datetime(2021, 1, 1),
                                          end_date=datetime.datetime(2025, 1, 1),
                                          warehouse_uid=warehouse.uid)
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        result = process.execute(transactions)
        assert result["Мука"]["beginning_balance"] == 90

    def test_end_balance(self):
        """
        Проверяет конечный баланс за период с 01.01.2021 по 01.01.2025
        Результатом сравнения должен быть 100
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=datetime.datetime(2021, 1, 1),
                                          end_date=datetime.datetime(2025, 1, 1),
                                          warehouse_uid=warehouse.uid)
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        result = process.execute(transactions)
        assert result["Мука"]["end_balance"] == 100

    def test_debit_credit(self):
        """
        Проверяет дебит за период с 01.01.2019 по 01.01.2021
        Результатом сравнения должен быть 100
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=datetime.datetime(2019, 1, 1),
                                          end_date=datetime.datetime(2021, 1, 1),
                                          warehouse_uid=warehouse.uid)
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        result = process.execute(transactions)
        assert result["Мука"]["debit"] == 100

    def test_credit_credit(self):
        """
        Проверяет кредит за период с 01.01.2019 по 01.01.2021
        Результатом сравнения должен быть 10
        :return:
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=datetime.datetime(2019, 1, 1),
                                          end_date=datetime.datetime(2021, 1, 1),
                                          warehouse_uid=warehouse.uid)
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        result = process.execute(transactions)
        assert result["Мука"]["credit"] == 10

    def test_save_balance_sheet_image(self):
        """
        Генерирует и сохраняет изображение ОСВ за период с 01.01.2021 по 01.01.2025
        """
        warehouse = self.repository.data[self.repository.warehouse_key()][0]
        process = ProcessFactory().create(ProcessType.BALANCE_SHEET,
                                          start_date=datetime.datetime(2021, 1, 1),
                                          end_date=datetime.datetime(2025, 1, 1),
                                          warehouse_uid=warehouse.uid)
        key = self.repository.warehouse_transaction_key()
        transactions = self.repository.data[key]
        result = process.execute(transactions)

        output_path = "../demo/balance_sheet_image.png"
        self.generate_balance_sheet_image(result, output_file=output_path)

        assert os.path.exists(output_path), "Файл изображения ОСВ не был создан"

    def generate_balance_sheet_image(self, balance_sheet, output_file="balance_sheet.png"):
        """
        Генерирует изображение таблицы ОСВ из данных balance_sheet.
        :param balance_sheet: Словарь с данными ОСВ
        :param output_file: Имя выходного файла изображения
        """
        # Преобразуем данные в DataFrame
        data = []
        for nomenclature, values in balance_sheet.items():
            data.append([
                nomenclature,
                values["beginning_balance"],
                values["debit"],
                values["credit"],
                values["end_balance"],
                values["measurement_unit"].name if values["measurement_unit"] else "N/A"
            ])

        columns = ["Номенклатура", "Начальный остаток", "Дебет", "Кредит", "Конечный остаток", "Ед. измерения"]
        df = pd.DataFrame(data, columns=columns)

        fig, ax = plt.subplots(figsize=(10, len(data) * 0.5 + 2))
        ax.axis("tight")
        ax.axis("off")
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))

        plt.savefig(output_file, bbox_inches="tight", dpi=300)
        plt.close(fig)
