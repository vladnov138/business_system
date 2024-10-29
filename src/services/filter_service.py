from src.dto.filter_dto import FilterDto
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.argument_exception import ArgumentException
from src.logics.model_prototype import ModelPrototype
from src.logics.warehouse_transaction_prototype import WarehouseTransactionPrototype


class FilterService:

    def filter(self, source: list, filter_dto: FilterDto) -> list:
        ArgumentException.check_arg(filter_dto, FilterDto)
        prototype = ModelPrototype(source)
        for item in filter_dto.items:
            prototype = prototype.create(item)
        return prototype.data

    def filter_warehouse_transactions(self, source: list, warehouse_filter_dto: WarehouseTransactionFilterDto) -> list:
        ArgumentException.check_arg(warehouse_filter_dto, WarehouseTransactionFilterDto)
        prototype = WarehouseTransactionPrototype(source)
        for filter_item in warehouse_filter_dto.items:
            prototype = prototype.create(filter_item)
        return prototype.data
