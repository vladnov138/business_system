from src.exceptions.operation_exception import OperationException
from src.logics.warehouse_turnover_process import WarehouseTurnoverProcess


class ProcessFactory:
    __processes = {}

    def __init__(self):
        self.__processes = {
            "warehouse_turnover": WarehouseTurnoverProcess.__name__
        }

    def create(self, process_name: str):
        if process_name in self.__processes.keys():
            return self.__processes[process_name]
        raise OperationException("Invalid process name")

    def process_names(self):
        return self.__processes.keys()