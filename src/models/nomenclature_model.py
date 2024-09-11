class NomenclatureModel:
    __full_name: str = ""

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        if isinstance(value, str) and len(value) <= 255:
            self.__full_name = value