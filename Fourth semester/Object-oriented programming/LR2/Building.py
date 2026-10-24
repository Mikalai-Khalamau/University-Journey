from abc import ABC, abstractmethod

class Building(ABC):
    def __init__(self, name, address):
        self.name = name
        self.address = address

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
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError("Address must be a string")
        self.__address = value.strip()

    @abstractmethod
    def get_building_type(self):
        pass

    @abstractmethod
    def get_occupancy_info(self):
        pass

    @abstractmethod
    def get_contact_info(self):
        pass

    def rename_building(self, new_name):
        try:
            self.name = new_name
            return True
        except:
            return False

    @abstractmethod
    def calculate_cost(self) -> float:
        pass