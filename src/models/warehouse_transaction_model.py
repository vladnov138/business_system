from __future__ import annotations

from datetime import datetime

from src.abstract.base_comparing_by_name import BaseComparingByName
from src.abstract.transaction_type import TransactionType
from src.exceptions.argument_exception import ArgumentException
from src.models.measurement_unit_model import MeasurementUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel


class WarehouseTransactionModel(BaseComparingByName):
    __warehouse: WarehouseModel = None
    __nomenclature: NomenclatureModel = None
    __amount: float = 0.0
    __measurement_unit: MeasurementUnitModel = None
    __transaction_type: TransactionType = None
    __period: datetime = None

    @classmethod
    def create(cls, name: str, warehouse: WarehouseModel, nomenclature: NomenclatureModel, amount: float | int,
               measurement_unit: MeasurementUnitModel, transaction_type: TransactionType, period: datetime):
        model = cls()
        model.name = name
        model.warehouse = warehouse
        model.nomenclature = nomenclature
        model.amount = amount
        model.measurement_unit = measurement_unit
        model.transaction_type = transaction_type
        model.period = period
        return model

    @staticmethod
    def default_income_transaction(warehouse: WarehouseModel, nomenclature: NomenclatureModel,
                                   measurement_unit: MeasurementUnitModel,
                                   period: datetime = datetime(2020, 1, 1)) -> WarehouseTransactionModel:
        name = "Поступление сырья"
        amount = 100
        transaction_type = TransactionType.INCOME
        transaction = WarehouseTransactionModel.create(name, warehouse, nomenclature, amount, measurement_unit,
                                                       transaction_type, period)
        return transaction

    @staticmethod
    def default_expense_transaction(warehouse: WarehouseModel, nomenclature: NomenclatureModel,
                                    measurement_unit: MeasurementUnitModel,
                                    period: datetime = datetime(2020, 1, 1)) -> WarehouseTransactionModel:
        name = "Расход сырья"
        amount = 10
        transaction_type = TransactionType.EXPENSE
        transaction = WarehouseTransactionModel.create(name, warehouse, nomenclature, amount, measurement_unit,
                                                       transaction_type, period)
        return transaction

    @property
    def warehouse(self) -> WarehouseModel:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        ArgumentException.check_arg(value, WarehouseModel)
        self.__warehouse = value

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        ArgumentException.check_arg(value, NomenclatureModel)
        self.__nomenclature = value

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float | int):
        if isinstance(value, int):
            value = float(value)
        ArgumentException.check_arg(value, float)
        self.__amount = value

    @property
    def measurement_unit(self) -> MeasurementUnitModel:
        return self.__measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnitModel):
        ArgumentException.check_arg(value, MeasurementUnitModel)
        self.__measurement_unit = value

    @property
    def transaction_type(self) -> TransactionType:
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value: TransactionType):
        ArgumentException.check_arg(value, TransactionType)
        self.__transaction_type = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value: datetime):
        ArgumentException.check_arg(value, datetime)
        self.__period = value
