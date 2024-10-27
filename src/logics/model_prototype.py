from src.abstract.abstract_prototype import AbstractPrototype
from src.abstract.filter_type import FilterType
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.filter_item import FilterItem


class ModelPrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)

    def __filter_nested(self, item: object, field_name: str, type_: FilterType, value: str) -> list:
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(item.__class__, x)),
                             dir(item)))
        result = []
        for field in fields:
            val = getattr(item, field)
            if isinstance(val, type(item)):
                prototype = ModelPrototype([val])
                res = prototype.create(field_name, type_, value)
                if len(res.data) > 0:
                    result.append(res)
        return result

    def create(self, field: str, filter_item: FilterItem):
        ArgumentException.check_arg(filter_item, FilterItem)
        type = filter_item.type
        value = filter_item.value
        condition = self._conditions.get(type) or None
        if condition is None:
            raise OperationException("Invalid filter type")
        result = []
        for item in self.data:
            field_value = getattr(item, field)
            if field_value is None:
                raise OperationException("Invalid field value")
            if condition(value, field_value):
                result.append(item)
            else:
                nested = self.__filter_nested(item, field, type, value)
                if len(nested) > 0:
                    result.append(item)
        prototype = ModelPrototype(result)
        return prototype
