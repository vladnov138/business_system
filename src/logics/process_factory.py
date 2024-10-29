from src.abstract.process_type import ProcessType
from src.exceptions.argument_exception import ArgumentException
from src.exceptions.operation_exception import OperationException
from src.logics.warehouse_turnover_process import WarehouseTurnoverProcess


class ProcessFactory:
    __processes = {}

    def __init__(self):
        self.__processes = {
            ProcessType.TURNOVER: WarehouseTurnoverProcess
        }

    def create(self, process_type: ProcessType):
        ArgumentException.check_arg(process_type, ProcessType)
        if process_type in self.__processes.keys():
            return self.__processes[process_type]()
        raise OperationException("Invalid process name")

    def process_names(self):
        return self.__processes.keys()