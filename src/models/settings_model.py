from datetime import datetime

from src.abstract.format_reporting import FormatReporting
from src.exceptions.argument_exception import ArgumentException


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

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 12)
        self.__inn = value

    @property
    def director_name(self):
        return self.__director_name

    @director_name.setter
    def director_name(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__director_name = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 11)
        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 11)
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 9)
        self.__bik = value

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 5)
        self.__business_type = value

    @property
    def recipe_folder(self):
        return self.__recipe_folder

    @recipe_folder.setter
    def recipe_folder(self, value):
        self.__recipe_folder = value

    @property
    def measurement_units_path(self):
        return self.__measurement_units_path

    @measurement_units_path.setter
    def measurement_units_path(self, value):
        self.__measurement_units_path = value

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: FormatReporting):
        ArgumentException.check_arg(value, FormatReporting)
        self.__report_format = value

    @property
    def format_reports(self):
        return self.__format_reports

    @format_reports.setter
    def format_reports(self, value: dict):
        ArgumentException.check_arg(value, dict)
        self.__format_reports = value

    @property
    def report_classes_folder(self):
        return self.__report_classes_folder

    @report_classes_folder.setter
    def report_classes_folder(self, value: str):
        ArgumentException.check_arg(value, str)
        self.__report_classes_folder = value

    @property
    def date_format(self):
        return self.__date_format

    @date_format.setter
    def date_format(self, value: str):
        self.__date_format = value

    @property
    def date_block(self):
        return self.__date_block

    @date_block.setter
    def date_block(self, value: datetime | str):
        if isinstance(value, str):
            value = datetime.strptime(value.split(" ")[0], self.date_format)
        ArgumentException.check_arg(value, datetime)
        self.__date_block = value

    def __str__(self):
        return f"""Settings(Organization Name: {self.organization_name}
                INN: {self.inn}
                Director Name: {self.director_name}
                Account: {self.account}
                Correspondent Account: {self.correspondent_account}
                BIK: {self.bik}
                Business Type: {self.business_type})"""