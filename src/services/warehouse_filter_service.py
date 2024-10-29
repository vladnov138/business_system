from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.argument_exception import ArgumentException
from src.logics.warehouse_transaction_prototype import WarehouseTransactionPrototype
from src.models.warehouse_transaction_model import WarehouseTransactionModel


class WarehouseTransactionFilterService:
    def create(self, data: list[WarehouseTransactionModel], filter_dto: WarehouseTransactionFilterDto):
        ArgumentException.check_arg(filter_dto, WarehouseTransactionFilterDto)
        for item in data:
            ArgumentException.check_arg(item, WarehouseTransactionModel)
        prototype = WarehouseTransactionPrototype(data)
        self.data = self.filter_warehouse(data, filter_dto)
        self.data = self.filter_nomenclature(self.data, filter_dto)
        self.data = self.filter_period(self.data, filter_dto)
        instance = WarehouseTransactionPrototype(self.data)
        return instance