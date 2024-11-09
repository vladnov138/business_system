from src.abstract.abstract_process import AbstractProcess
from src.abstract.transaction_type import TransactionType
from src.exceptions.argument_exception import ArgumentException
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.models.warehouse_turnover_model import WarehouseTurnOverModel


class WarehouseTurnoverProcess(AbstractProcess):
    def execute(self, transactions: list[WarehouseTransactionModel]) -> list[WarehouseTurnOverModel]:
        ArgumentException.check_arg(transactions, list)
        result = []

        grouped_transactions = {}
        for transaction in transactions:
            ArgumentException.check_arg(transaction, WarehouseTransactionModel)
            key = f"{transaction.nomenclature.uid}_{transaction.warehouse.uid}_{transaction.measurement_unit.uid}"
            if key not in grouped_transactions.keys():
                grouped_transactions[key] = []

            grouped_transactions[key].append(transaction)

        for key, transactions in grouped_transactions.items():
            first_transaction = transactions[0]
            turnover = (sum(transaction.amount for transaction in transactions if transaction.transaction_type == TransactionType.INCOME)
                        - sum(transaction.amount for transaction in transactions if transaction.transaction_type == TransactionType.EXPENSE))
            row = WarehouseTurnOverModel.create(first_transaction.warehouse, turnover, first_transaction.nomenclature,
                                        first_transaction.measurement_unit)
            result.append(row)
        return result
