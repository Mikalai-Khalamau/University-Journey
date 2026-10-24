from typing import List

class AcademyBuilding:
    def __init__(self, name: str, address: str, telephone_number: str, number: int):
        self.name = name
        self.address = address
        self.telephone_number = telephone_number
        self.number = number
        self.__departments: List[str] = []
        self.__staff: List[str] = []

    @property
    def name(self) -> str:
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
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError("Address must be a string")
        self.__address = value.strip()

    @property
    def telephone_number(self) -> str:
        return self.__telephone_number

    @telephone_number.setter
    def telephone_number(self, value):
        if not isinstance(value, str):
            raise TypeError("Telephone number must be a string")
        clean = value.strip()
        if len(clean) < 7:
            raise ValueError("Telephone number must have at least 7 digits")
        self.__telephone_number = clean

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError("Number must be an integer")
        if value < 1 or value > 20:
            raise ValueError("Number must be between 1 and 20")
        self.__number = value

    @property
    def departments(self) -> List[str]:
        return self.__departments.copy()

    @property
    def staff(self) -> List[str]:
        return self.__staff.copy()

    def add_department(self, department_name: str) -> bool:
        clean = department_name.strip()
        if len(clean) < 2 or clean in self.__departments:
            return False
        self.__departments.append(clean)
        return True

    def remove_department(self, department_name: str) -> bool:
        clean = department_name.strip()
        if clean in self.__departments:
            self.__departments.remove(clean)
            return True
        return False

    def add_staff(self, staff_name: str) -> bool:
        clean = staff_name.strip()
        if len(clean) < 2 or clean in self.__staff:
            return False
        self.__staff.append(clean)
        return True

    def remove_staff(self, staff_name: str) -> bool:
        clean = staff_name.strip()
        if clean in self.__staff:
            self.__staff.remove(clean)
            return True
        return False

    def rename_building(self, new_name: str) -> bool:
        clean = new_name.strip()
        if len(clean) < 2:
            return False
        self.name = clean
        return True

    def is_understaffed(self, threshold: int = 5) -> bool:
        if not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Threshold must be a positive integer")
        return len(self.__staff) < threshold