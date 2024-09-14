from src.exceptions.argument_exception import ArgumentException
from src.utils.checker import check_arg, check_exact_length, check_max_len


class Settings:
    __organization_name = ""
    __inn = ""
    __director_name = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __business_type = ""

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        check_arg(value, str)
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 12)
        self.__inn = value

    @property
    def director_name(self):
        return self.__director_name

    @director_name.setter
    def director_name(self, value: str):
        check_arg(value, str)
        self.__director_name = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 11)
        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        check_arg(value, str)
        check_exact_length(value, 11)
        self.__correspondent_account = value

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

    def __str__(self):
        return f"""Settings(Organization Name: {self.organization_name}
                INN: {self.inn}
                Director Name: {self.director_name}
                Account: {self.account}
                Correspondent Account: {self.correspondent_account}
                BIK: {self.bik}
                Business Type: {self.business_type})"""