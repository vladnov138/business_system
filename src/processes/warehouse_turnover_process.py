from src.abstract.abstract_process import AbstractProcess
from src.abstract.transaction_type import TransactionType
from src.exceptions.argument_exception import ArgumentException
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.models.warehouse_turnover_model import WarehouseTurnOverModel


class WarehouseTurnoverProcess(AbstractProcess):
    def execute(self, transactions: list[WarehouseTransactionModel]) -> list[WarehouseTurnOverModel]:
        result = {}
        for transaction in transactions:
            ArgumentException.check_arg(transaction, WarehouseTransactionModel)
            warehouse = transaction.warehouse
            nomenclature = transaction.nomenclature
            measurement_unit = transaction.measurement_unit
            key = (warehouse, nomenclature, measurement_unit)
            value = transaction.amount
            if transaction.transaction_type == TransactionType.EXPENSE:
                value = -value
            result[key] = result.get(key, 0) + value
        turns = []
        for key, value in result.items():
            turn = WarehouseTurnOverModel.create(warehouse=key[0], turnover=value, nomenclature=key[1],
                                                 measurement_unit=key[2])
            turns.append(turn)
        return turns
