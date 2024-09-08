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
        if not isinstance(value, str):
            raise TypeError("Invalid value")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str) or len(value) != 12:
            raise ValueError("INN must be a 12-character string")
        self.__inn = value

    @property
    def director_name(self):
        return self.__director_name

    @director_name.setter
    def director_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Invalid value")
        self.__director_name = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise ValueError("Account must be an 11-character string")
        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise ValueError("Correspondent account must be an 11-character string")
        self.__correspondent_account = value

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
            raise ValueError("Ownership type must be a 5-character string")
        self.__business_type = value