from src.abstract.filter_type import FilterType


class FilterDto:
    __name: str = ""
    __id: str = ""
    __type: FilterType = None

    @classmethod
    def create(cls, id, name, type):
        filter_dto = cls()
        filter_dto.id = id
        filter_dto.name = name
        filter_dto.type = FilterType(type)
        return filter_dto

    @classmethod
    def from_json(cls, json_data):
        id = json_data.get("id")
        name = json_data.get("name")
        type = json_data.get("type")
        if isinstance(type, str):
            type = FilterType[type.upper()]
        return cls.create(id, name, type)

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