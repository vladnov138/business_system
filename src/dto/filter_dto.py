from src.abstract.filter_type import FilterType


class FilterDto:
    __name: str = ""
    __id: str = ""
    __type: FilterType = None

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = FilterType(type)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: FilterType):
        self.__type = value