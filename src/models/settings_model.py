from datetime import datetime

from src.abstract.format_reporting import FormatReporting
from src.core.event_type import EventType
from src.exceptions.argument_exception import ArgumentException
from src.logger.log_level import LogLevel
from src.services.observe_service import ObserveService


class Settings:
    __organization_name = ""
    __inn = ""
    __director_name = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __business_type = ""

    __recipe_folder = ""
    __measurement_units_path = ""

    __report_format: FormatReporting = None
    __format_reports: dict = {}
    __report_classes_folder = ""

    __date_format = "%Y-%m-%d"
    __date_block = None

    __generate_data = True
    __data_file: str = "data_repository.json"

    __log_level: LogLevel = None
    __log_path: str = None

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__organization_name = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: organization_name changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            ArgumentException.check_exact_length(value, 12)
            self.__inn = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: inn changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def director_name(self):
        return self.__director_name

    @director_name.setter
    def director_name(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__director_name = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: director_name changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            ArgumentException.check_exact_length(value, 11)
            self.__account = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: account changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            ArgumentException.check_exact_length(value, 11)
            self.__correspondent_account = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: correspondent_account changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            ArgumentException.check_exact_length(value, 9)
            self.__bik = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: bik changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            ArgumentException.check_exact_length(value, 5)
            self.__business_type = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: business_type changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def recipe_folder(self):
        return self.__recipe_folder

    @recipe_folder.setter
    def recipe_folder(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__recipe_folder = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: recipe_folder changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def measurement_units_path(self):
        return self.__measurement_units_path

    @measurement_units_path.setter
    def measurement_units_path(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__measurement_units_path = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: measurement_units_path changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: FormatReporting):
        try:
            ArgumentException.check_arg(value, FormatReporting)
            self.__report_format = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: report_format changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def format_reports(self):
        return self.__format_reports

    @format_reports.setter
    def format_reports(self, value: dict):
        try:
            ArgumentException.check_arg(value, dict)
            self.__format_reports = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: format_reports changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def report_classes_folder(self):
        return self.__report_classes_folder

    @report_classes_folder.setter
    def report_classes_folder(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__report_classes_folder = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: report_classes_folder changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def date_format(self):
        return self.__date_format

    @date_format.setter
    def date_format(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__date_format = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: date_format changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def date_block(self):
        return self.__date_block

    @date_block.setter
    def date_block(self, value: datetime | str):
        try:
            if isinstance(value, str):
                value = datetime.strptime(value.split(" ")[0], self.date_format)
            ArgumentException.check_arg(value, datetime)
            self.__date_block = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: date_block changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def generate_data(self):
        return self.__generate_data

    @generate_data.setter
    def generate_data(self, value: bool):
        try:
            ArgumentException.check_arg(value, bool)
            self.__generate_data = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: generate_data changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value: str):
        try:
            ArgumentException.check_arg(value, str)
            self.__data_file = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: data_file changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def log_level(self):
        return self.__log_level

    @log_level.setter
    def log_level(self, value: LogLevel):
        try:
            ArgumentException.check_arg(value, LogLevel)
            self.__log_level = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: log_level changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    @property
    def log_path(self):
        return self.__log_path

    @log_path.setter
    def log_path(self, value: str | None):
        try:
            ArgumentException.check_arg(value, str, True)
            self.__log_path = value
            ObserveService.raise_event(EventType.LOG_INFO, message=f"Settings: log_path changed to {value}")
        except Exception as ex:
            ObserveService.raise_event(EventType.LOG_ERROR, message=ex)

    def __str__(self):
        return f"""Settings(Organization Name: {self.organization_name}
                INN: {self.inn}
                Director Name: {self.director_name}
                Account: {self.account}
                Correspondent Account: {self.correspondent_account}
                BIK: {self.bik}
                Business Type: {self.business_type})"""