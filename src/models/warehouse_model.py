from __future__ import annotations

from src.abstract.base_comparing_by_name import BaseComparingByName


class WarehouseModel(BaseComparingByName):
    __address = None

    @classmethod
    def create(cls, name: str, address: str):
        model = cls()
        model.name = name
        model.address = address
        return model

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @staticmethod
    def default_warehouse() -> WarehouseModel:
        name = "Склад"
        address = "Россия, Московская область, г. Москва, ул. Профсоюзная, д. 15"
        warehouse = WarehouseModel.create(name, address)
        return warehouse