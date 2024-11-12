from datetime import datetime

from src.abstract.process_type import ProcessType
from src.data.data_repository import DataRepository
from src.exceptions.argument_exception import ArgumentException
from src.processes.process_factory import ProcessFactory


class DateBlockUpdator:
    """
    Класс-слушатель, совершает действия при изменении date_block
    """
    __dateblock: datetime = None
    __repository: DataRepository = None
    __process_factory: ProcessFactory = None
    __process_type: ProcessType = None

    def __init__(self, dateblock: datetime, repository: DataRepository, process_factory: ProcessFactory, process_type: ProcessType):
        ArgumentException.check_arg(dateblock, datetime)
        self.__dateblock = dateblock
        ArgumentException.check_arg(repository, DataRepository)
        self.__repository = repository
        ArgumentException.check_arg(process_factory, ProcessFactory)
        self.__process_factory = process_factory
        ArgumentException.check_arg(process_type, ProcessType)
        self.__process_type = process_type

    def update(self, dateblock: datetime):
        ArgumentException.check_arg(dateblock, datetime)
        transaction_key = self.__repository.warehouse_transaction_key()
        transactions = self.__repository.data[transaction_key]
        turnover_key = self.__repository.turnovers_key()
        turnovers = self.__repository.data[turnover_key]
        process = self.__process_factory.create(self.__process_type, turnovers=turnovers, dateblock=self.__dateblock)
        result = process.execute(transactions)
        self.__repository.data[turnover_key] = result
        self.__dateblock = dateblock