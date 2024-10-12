from src.abstract.abstract_prototype import AbstractPrototype
from src.abstract.filter_type import FilterType
from src.dto.filter_dto import FilterDto
from src.exceptions.operation_exception import OperationException


class ModelPrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)
        self.conditions = {
            FilterType.EQUAL: lambda searched_text, text: searched_text == text,
            FilterType.LIKE: lambda searched_text, text: searched_text in text
        }

    def create(self, data: list, filter_dto: FilterDto):
        super().create(data, filter_dto)
        self.data = self.filter_name(data, filter_dto)
        self.data = self.filter_id(self.data, filter_dto)
        instance = ModelPrototype(self.data)
        return instance

    def filter_name(self, source: list, filter_dto: FilterDto) -> list :
        if filter_dto.name == "" or filter_dto.name is None:
            return source
        condition = self.conditions.get(filter_dto.type) or None
        if condition is None:
            raise OperationException("Invalid filter type")
        result = []
        for item in source:
            if condition(filter_dto.name, item.name):
                result.append(item)
        return result

    def filter_id(self, source: list, filter_dto: FilterDto) -> list:
        if filter_dto.id == "" or filter_dto.id is None:
            return source
        condition = self.conditions.get(filter_dto.type) or None
        if condition is None:
            raise OperationException("Invalid filter type")
        result = []
        for item in source:
            if condition(filter_dto.id, item.uid):
                result.append(item)
        return result
