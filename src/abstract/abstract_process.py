from abc import ABC, abstractmethod

from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.models.warehouse_turnover_model import WarehouseTurnOverModel


class AbstractProcess(ABC):

    @abstractmethod
    def execute(self, transactions: list[WarehouseTransactionModel]) -> list[WarehouseTurnOverModel]:
        pass
