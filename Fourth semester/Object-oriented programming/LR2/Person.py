from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, passport_details, telephone_number):
        self.name = name
        self.passport_details = passport_details
        self.telephone_number = telephone_number

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Name must have at least 2 characters")
        self.__name = clean

    @property
    def passport_details(self):
        return self.__passport_details

    @passport_details.setter
    def passport_details(self, value):
        if not isinstance(value, str):
            raise TypeError("Passport details must be a string")
        self.__passport_details = value.strip()

    @property
    def telephone_number(self):
        return self.__telephone_number

    @telephone_number.setter
    def telephone_number(self, value):
        if not isinstance(value, str):
            raise TypeError("Telephone number must be a string")
        clean = value.strip()
        if len(clean) < 7:
            raise ValueError("Telephone number must have at least 7 digits")
        self.__telephone_number = clean

    @abstractmethod
    def get_role_description(self):
        pass

    @abstractmethod
    def get_contact_info(self):
        pass

    def update_contact_info(self, telephone_number = None, email = None):
        if telephone_number:
            self.telephone_number = telephone_number
        return True