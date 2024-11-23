from datetime import datetime

from src.abstract.abstract_logic import AbstractLogic
from src.core.event_type import EventType
from src.exceptions.argument_exception import ArgumentException
from src.logger.log_level import LogLevel


class Logger(AbstractLogic):
    __log_path = None
    __log_level: LogLevel = None
    __event_to_log = {
        EventType.LOG_INFO: LogLevel.INFO,
        EventType.LOG_DEBUG: LogLevel.DEBUG,
        EventType.LOG_ERROR: LogLevel.ERROR
    }

    def __init__(self, log_path: str | None, log_level: LogLevel):
        ArgumentException.check_arg(log_path, str, True)
        ArgumentException.check_arg(log_level, LogLevel)
        self.__log_level = log_level
        if log_path is not None:
            self.__log_path = log_path
            self.__init_log_file()

    def __init_log_file(self):
        with open(self.__log_path, 'w') as file:
            file.write(f"---Logger started at {datetime.now().isoformat()}---")
            file.write(f"\n---Logger level: {self.__log_level}---")

    def __log(self, type: LogLevel, msg: str):
        message = f"\n[{datetime.now().isoformat()} | {type.name}]: {msg}"
        if self.__log_path is not None:
            with open(self.__log_path, 'a') as file:
                file.write(message)
        else:
            print(message)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, **kwargs):
        super().handle_event(type, **kwargs)
        if type not in (EventType.LOG_INFO, EventType.LOG_DEBUG, EventType.LOG_ERROR):
            return
        try:
            ArgumentException.check_arg(kwargs.get("message"), str)
        except Exception as e:
            raise ArgumentException("Invalid arguments in kwargs") from e
        message = kwargs["message"]
        self.__log(self.__event_to_log[type], message)
