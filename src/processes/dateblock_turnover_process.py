from datetime import datetime

from src.abstract.abstract_process import AbstractProcess
from src.abstract.date_filter_type import DateFilterType
from src.abstract.period_filter_item import PeriodFilterItem
from src.dto.warehouse_transaction_filter_dto import WarehouseTransactionFilterDto
from src.exceptions.argument_exception import ArgumentException
from src.logics.warehouse_filter_item import WarehouseFilterItem
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.models.warehouse_turnover_model import WarehouseTurnOverModel
from src.processes.warehouse_turnover_process import WarehouseTurnoverProcess
from src.services.filter_service import FilterService


class DateBlockTurnoverProcess(AbstractProcess):
    __dateblock: datetime = None
    __turnovers: list[WarehouseTurnOverModel] = None

    def __init__(self, dateblock: datetime, turnovers: list[WarehouseTurnOverModel]):
        super().__init__()
        if turnovers is not None:
            for turnover in turnovers:
                ArgumentException.check_arg(turnover, WarehouseTurnOverModel)
        self.__turnovers = turnovers
        ArgumentException.check_arg(dateblock, datetime)
        self.__dateblock = dateblock

    def execute(self, transactions: list[WarehouseTransactionModel]) -> list[WarehouseTurnOverModel]:
        # Фильтруем транзакции: отбрасываем те, которые были до dateblock, т.к. они посчитаны
        filter_items = []
        filter_item_after = WarehouseFilterItem()
        curr_dateblock_filter_item = PeriodFilterItem()
        curr_dateblock_filter_item.date = self.__dateblock
        curr_dateblock_filter_item.filter_type = DateFilterType.AFTER
        filter_item_after.period = curr_dateblock_filter_item
        filter_items.append(filter_item_after)
        filter_dto = WarehouseTransactionFilterDto.create(filter_items)

        filter_service = FilterService()
        filtered_transactions = filter_service.filter_warehouse_transactions(transactions, filter_dto)

        new_turnovers = WarehouseTurnoverProcess().execute(filtered_transactions)

        # группировка
        result = []
        for item in new_turnovers:
            is_turnover_found = False
            for idx in range(len(self.__turnovers)):
                turnover = self.__turnovers[idx]
                if turnover.warehouse == item.warehouse and turnover.nomenclature == turnover.nomenclature \
                    and turnover.measurement_unit == item.measurement_unit:
                    self.__turnovers[idx].turnover += item.turnover
                    is_turnover_found = True
                    break
            if not is_turnover_found:
                result.append(item)
        self.__turnovers += result
        return self.__turnovers
