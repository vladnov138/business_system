from src.abstract.abstract_prototype import AbstractPrototype
from src.abstract.filter_type import FilterType
from src.dto.filter_dto import FilterDto
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.operation_exception import OperationException


class WarehouseTransactionPrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)

    def __filter(self, field: str, source: list, searched_value) -> list:
        result = []
        for item in source:
            field_value = getattr(item, field)
            if field_value is None:
                raise OperationException("Invalid field value")
            if field_value == searched_value:
                result.append(item)
        return result

    def filter_warehouse(self, source: list, filter_dto: WarehouseTransactionFilterDto) -> list:
        if filter_dto.warehouse is None:
            return source
        return self.__filter("warehouse", source, filter_dto.warehouse)

    def filter_nomenclature(self, source: list, filter_dto: WarehouseTransactionFilterDto) -> list:
        if filter_dto.nomenclature is None:
            return source
        return self.__filter("nomenclature", source, filter_dto.nomenclature)

    def create(self, data: list, filter_dto: WarehouseTransactionFilterDto):
        super().create(data, filter_dto)
        self.data = self.filter_warehouse(data, filter_dto)
        self.data = self.filter_nomenclature(self.data, filter_dto)
        instance = WarehouseTransactionPrototype(self.data)
        return instance
