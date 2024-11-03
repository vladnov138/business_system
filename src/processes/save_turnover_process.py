from src.abstract.abstract_process import AbstractProcess
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.models.warehouse_turnover_model import WarehouseTurnOverModel


class SaveTurnoverProcess(AbstractProcess):
  def execute(self, transactions: list[WarehouseTransactionModel]) -> list[WarehouseTurnOverModel]:
    pass