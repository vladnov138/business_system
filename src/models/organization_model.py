from src.abstract_reference import AbstractReference
from src.exceptions.argument_exception import ArgumentException
from src.models.settings_model import Settings


class OrganizationModel(AbstractReference):
    __inn = ""
    __account = ""
    __bik = ""
    __business_type = ""

    def __init__(self, settings: Settings):
        super().__init__(settings.organization_name)
        self.__inn = settings.inn
        self.__account = settings.account
        self.__bik = settings.bik
        self.__business_type = settings.business_type

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

    def __eq__(self, other):
        if not isinstance(other, OrganizationModel):
            return False
        return self._name == other._name

    def __ne__(self, other):
        return not self == other
