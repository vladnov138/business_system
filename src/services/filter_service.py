from src.dto.filter_dto import FilterDto
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.logics.model_prototype import ModelPrototype
from src.logics.warehouse_transaction_prototype import WarehouseTransactionPrototype


class FilterService:

    def filter(self, source: list, filter_dto: FilterDto) -> list:
        prototype = ModelPrototype(source)
        for item in filter_dto.items:
            prototype = prototype.create(item.field, item.type, item.value)
        return prototype.data

    def filter_warehouse_transactions(self, source: list, warehouse_filter_dto: WarehouseTransactionFilterDto) -> list:
        prototype = WarehouseTransactionPrototype(source)
        for filter_item in warehouse_filter_dto.items:
            prototype = prototype.create(filter_item)
        return prototype.data
