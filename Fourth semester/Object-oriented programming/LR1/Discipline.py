from typing import List
from LR1.Teacher import Teacher

class Discipline:
    def __init__(self, name: str, hours: int):
        self.name = name
        self.hours = hours
        self.__teachers: List[str] = []

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
    def hours(self) -> int:
        return self.__hours

    @hours.setter
    def hours(self, value):
        if not isinstance(value, int):
            raise TypeError("Hours must be an integer")
        if value < 16 or value > 300:
            raise ValueError("Hours must be between 16 and 300")
        self.__hours = value

    @property
    def teachers(self) -> List[str]:
        return self.__teachers.copy()

    def add_teacher(self, teacher_name: str) -> bool:
        clean = teacher_name.strip()
        if len(clean) < 2 or clean in self.__teachers:
            return False
        self.__teachers.append(clean)
        return True

    def remove_teacher(self, teacher_name: str) -> bool:
        clean = teacher_name.strip()
        if clean in self.__teachers:
            self.__teachers.remove(clean)
            return True
        return False

    def is_heavyload(self) -> bool:
        return self.hours > 100

    def assign_teacher(self, teacher: Teacher) -> bool:
        return self.add_teacher(teacher.name)