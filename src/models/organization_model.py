from src.abstract_reference import AbstractReference
from src.models.settings_model import Settings
from src.utils.checker import check_arg, check_max_len, check_exact_length


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
        check_arg(value, str)
        check_exact_length(value, 12)
        self.__inn = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 11)
        self.__account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 9)
        self.__bik = value

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 5)
        self.__business_type = value
