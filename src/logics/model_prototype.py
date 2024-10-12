from src.abstract.abstract_prototype import AbstractPrototype
from src.abstract.filter_type import FilterType
from src.dto.filter_dto import FilterDto
from src.exceptions.operation_exception import OperationException


class ModelPrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)

    def create(self, data: list, filter_dto: FilterDto):
        super().create(data, filter_dto)
        self.data = self.filter_name(data, filter_dto)
        self.data = self.filter_id(self.data, filter_dto)
        instance = ModelPrototype(self.data)
        return instance

    def filter_name(self, source: list, filter_dto: FilterDto) -> list :
        if filter_dto.name == "" or filter_dto.name is None:
            return source
        if filter_dto.type == FilterType.EQUAL:
            return self.__filter_equal_name(source, filter_dto)
        elif filter_dto.type == FilterType.LIKE:
            return self.__filter_like_name(source, filter_dto)
        raise OperationException("Invalid type")

    def __filter_equal_name(self, source: list, filter_dto: FilterDto) -> list:
        result = []
        for item in source:
            if item.name == filter_dto.name:
                result.append(item)
            fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(item.__class__, x)),
                                 dir(item)))
            for field in fields:
                val = getattr(item, field)
                if hasattr(val, '__dict__') and isinstance(val, type(item)):
                    result.append(*self.__filter_equal_name([val], filter_dto))
        return result

    def __filter_like_name(self, source: list, filter_dto: FilterDto) -> list:
        result = []
        for item in source:
            if filter_dto.name in item.name:
                result.append(item)
        return result

    def filter_id(self, source: list, filter_dto: FilterDto) -> list:
        if filter_dto.id == "" or filter_dto.id is None:
            return source
        if filter_dto.type == FilterType.EQUAL:
            return self.__filter_equal_id(source, filter_dto)
        elif filter_dto.type == FilterType.LIKE:
            return self.__filter_like_id(source, filter_dto)
        raise OperationException("invalid_type")

    def __filter_equal_id(self, source: list, filter_dto: FilterDto) -> list:
        result = []
        for item in source:
            if item.id == filter_dto.id:
                result.append(item)
        return result

    def __filter_like_id(self, source: list, filter_dto: FilterDto) -> list:
        result = []
        for item in source:
            if filter_dto.id in item.id:
                result.append(item)
        return result
