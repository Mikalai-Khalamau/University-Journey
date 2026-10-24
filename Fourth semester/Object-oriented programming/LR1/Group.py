from typing import List

class Group:
    def __init__(self, number: int, speciality: str):
        self.number = number
        self.speciality = speciality
        self.__students: List[str] = []
        self.__disciplines: List[str] = []

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError("Number must be an integer")
        if value < 100000:
            raise ValueError("Group number must be at least 100000")
        self.__number = value

    @property
    def speciality(self) -> str:
        return self.__speciality

    @speciality.setter
    def speciality(self, value):
        if not isinstance(value, str):
            raise TypeError("Speciality must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Speciality name must have at least 2 characters")
        self.__speciality = clean

    @property
    def students(self) -> List[str]:
        return self.__students.copy()

    @property
    def disciplines(self) -> List[str]:
        return self.__disciplines.copy()

    def add_student(self, student_name: str) -> bool:
        clean = student_name.strip()
        if len(clean) < 2 or clean in self.__students:
            return False
        self.__students.append(clean)
        return True

    def remove_student(self, student_name: str) -> bool:
        clean = student_name.strip()
        if clean in self.__students:
            self.__students.remove(clean)
            return True
        return False

    def add_discipline(self, discipline: str) -> bool:
        clean = discipline.strip()
        if len(clean) < 2 or clean in self.__disciplines:
            return False
        self.__disciplines.append(clean)
        return True

    def remove_discipline(self, discipline: str) -> bool:
        clean = discipline.strip()
        if clean in self.__disciplines:
            self.__disciplines.remove(clean)
            return True
        return False

