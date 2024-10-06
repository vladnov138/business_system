from src.abstract.base_comparing_by_name import BaseComparingByName
from src.exceptions.argument_exception import ArgumentException
from src.models.settings_model import Settings


class OrganizationModel(BaseComparingByName):
    __inn = ""
    __account = ""
    __bik = ""
    __business_type = ""

    @classmethod
    def create(cls, settings: Settings):
        model = cls()
        model.name = settings.organization_name
        model.inn = settings.inn
        model.account = settings.account
        model.bik = settings.bik
        model.business_type = settings.business_type
        return model

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 12)
        self.__inn = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        ArgumentException.check_arg(value, str)
        ArgumentException.check_exact_length(value, 11)
        self.__account = value

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
