from src.models.settings_model import Settings


class Organization:
    __inn = ""
    __account = ""
    __bik = ""
    __business_type = ""

    def __init__(self, settings: Settings):
        self.__inn = settings.inn
        self.__account = settings.account
        self.__bik = settings.bik
        self.__business_type = settings.business_type

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str) or len(value) != 12:
            raise ValueError("INN must be a 12-character string")
        self.__inn = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise ValueError("Account must be an 11-character string")
        self.__account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str) or len(value) != 9:
            raise ValueError("BIK must be a 9-character string")
        self.__bik = value

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        if not isinstance(value, str) or len(value) != 5:
            raise ValueError("Businesstype type must be a 5-character string")
        self.__business_type = value
