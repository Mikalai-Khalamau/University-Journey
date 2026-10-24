from typing import List

class Dormitory:
    def __init__(self, name: str, address: str, telephone_number: str, number: int, capacity: int):
        self.name = name
        self.address = address
        self.telephone_number = telephone_number
        self.number = number
        self.capacity = capacity
        self.__students: List[str] = []
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
        if value < 1 or value > 10:
            raise ValueError("Number must be between 1 and 10")
        self.__number = value

    @property
    def capacity(self) -> int:
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value < 50 or value > 2000:
            raise ValueError("Capacity must be between 50 and 2000")
        self.__capacity = value

    @property
    def students(self) -> List[str]:
        return self.__students.copy()

    @property
    def staff(self) -> List[str]:
        return self.__staff.copy()

    def add_student(self, student_name: str) -> bool:
        clean = student_name.strip()
        if len(clean) < 2:
            raise ValueError("Student name must have at least 2 characters")
        if len(self.__students) >= self.__capacity:
            return False
        if clean in self.__students:
            return False
        self.__students.append(clean)
        return True

    def remove_student(self, student_name: str) -> bool:
        clean = student_name.strip()
        if clean in self.__students:
            self.__students.remove(clean)
            return True
        return False

    def hire_staff(self, staff_name: str) -> bool:
        clean = staff_name.strip()
        if len(clean) < 2:
            raise ValueError("Staff name must have at least 2 characters")
        if clean in self.__staff:
            return False
        self.__staff.append(clean)
        return True

    def fire_staff(self, staff_name: str) -> bool:
        clean = staff_name.strip()
        if clean in self.__staff:
            self.__staff.remove(clean)
            return True
        return False

    def expand_capacity(self, additional_places: int) -> bool:
        if additional_places <= 0:
            return False
        self.__capacity += additional_places
        return True