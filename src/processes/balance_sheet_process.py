from datetime import datetime

from src.abstract.abstract_process import AbstractProcess
from src.abstract.date_filter_type import DateFilterType
from src.abstract.filter_type import FilterType
from src.abstract.period_filter_item import PeriodFilterItem
from src.abstract.transaction_type import TransactionType
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.argument_exception import ArgumentException
from src.logics.filter_item import FilterItem
from src.logics.warehouse_filter_item import WarehouseFilterItem
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.services.filter_service import FilterService


class BalanceSheetProcess(AbstractProcess):
    """
    Класс для составления Оборотно-Сальдовой Ведомости
    """
    __warehouse_uid = None
    __start_date = None
    __end_date = None

    def __init__(self, warehouse_uid: str, start_date: datetime, end_date: datetime):
        ArgumentException.check_arg(warehouse_uid, str)
        ArgumentException.check_arg(start_date, datetime)
        ArgumentException.check_arg(end_date, datetime)
        self.__warehouse_uid = warehouse_uid
        self.__start_date = start_date
        self.__end_date = end_date

    def execute(self, transactions: list[WarehouseTransactionModel]):
        filter_item_beginning = WarehouseFilterItem()
        filter_item_beginning.warehouse_item = FilterItem.create("uid", FilterType.EQUAL, self.__warehouse_uid)
        filter_item_beginning.period = PeriodFilterItem.create(self.__start_date, DateFilterType.BEFORE)
        # Фильтруем транзакции: отбрасываем те, которые не с нашего склада
        filter_item_after = WarehouseFilterItem()
        filter_item_after.warehouse_item = FilterItem.create("uid", FilterType.EQUAL, self.__warehouse_uid)
        filter_item_after.period = PeriodFilterItem.create(self.__start_date, DateFilterType.AFTER)
        filter_item_after_equal = WarehouseFilterItem()
        filter_item_after_equal.period = PeriodFilterItem.create(self.__start_date, DateFilterType.EQUAL)
        filter_item_before = WarehouseFilterItem()
        filter_item_before.period = PeriodFilterItem.create(self.__end_date, DateFilterType.BEFORE)
        filter_items = [filter_item_after, filter_item_before]
        filter_dto = WarehouseTransactionFilterDto.create(filter_items)

        filter_service = FilterService()
        beginning_filter_dto = WarehouseTransactionFilterDto.create([filter_item_beginning])
        beginning_transactions = filter_service.filter_warehouse_transactions(transactions, beginning_filter_dto)
        filtered_transactions = filter_service.filter_warehouse_transactions(transactions, filter_dto)

        balance_sheet = {}
        for transaction in beginning_transactions:
            nomenclature = transaction.nomenclature.name
            amount = transaction.amount
            transaction_type = transaction.transaction_type
            if nomenclature not in balance_sheet:
                balance_sheet[nomenclature] = {
                    "debit": 0.0,
                    "credit": 0.0,
                    "beginning_balance": 0.0,
                    "end_balance": 0.0,
                    "measurement_unit": transaction.measurement_unit,
                }
            if transaction_type == TransactionType.INCOME:
                balance_sheet[nomenclature]["beginning_balance"] += amount
            elif transaction_type == TransactionType.EXPENSE:
                balance_sheet[nomenclature]["beginning_balance"] -= amount

        for transaction in filtered_transactions:
            nomenclature = transaction.nomenclature.name
            amount = transaction.amount
            transaction_type = transaction.transaction_type

            if nomenclature not in balance_sheet:
                balance_sheet[nomenclature] = {
                    "debit": 0.0,
                    "credit": 0.0,
                    "beginning_balance": 0.0,
                    "end_balance": 0.0,
                    "measurement_unit": transaction.measurement_unit,
                }

            if transaction_type == TransactionType.INCOME:
                balance_sheet[nomenclature]["debit"] += amount
                balance_sheet[nomenclature]["end_balance"] += amount
            elif transaction_type == TransactionType.EXPENSE:
                balance_sheet[nomenclature]["credit"] += amount
                balance_sheet[nomenclature]["end_balance"] -= amount

        return balance_sheet
