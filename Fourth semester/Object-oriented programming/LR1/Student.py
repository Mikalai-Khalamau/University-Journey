from typing import Dict, List

class Student:
    def __init__(self, name: str, age: int, course: int, group_number: int):
        self.name = name
        self.age = age
        self.course = course
        self.group_number = group_number
        self.dormitory_number = None
        self.__grades: Dict[str, List[float]] = {}

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
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 16 or value > 100:
            raise ValueError("Age must be between 16 and 100")
        self.__age = value

    @property
    def course(self) -> int:
        return self.__course

    @course.setter
    def course(self, value):
        if not isinstance(value, int):
            raise TypeError("Course must be an integer")
        if value < 1 or value > 6:
            raise ValueError("Course must be between 1 and 6")
        self.__course = value

    @property
    def group_number(self) -> int:
        return self.__group_number

    @group_number.setter
    def group_number(self, value):
        if not isinstance(value, int):
            raise TypeError("Group number must be an integer")
        if value < 100000:
            raise ValueError("Group number must be at least 100000")
        self.__group_number = value

    @property
    def gpa(self) -> float:
        if not self.__grades:
            return 0.0
        all_grades = [g for grades in self.__grades.values() for g in grades]
        return round(sum(all_grades) / len(all_grades), 2)

    def add_grade(self, discipline: str, grade) -> bool:
        if not isinstance(grade, (int, float)):
            raise TypeError("Grade must be a number")
        if not (1 <= grade <= 10):
            raise ValueError("Grade must be between 1 and 10")
        clean_disc = discipline.strip()
        if clean_disc not in self.__grades:
            self.__grades[clean_disc] = []
        self.__grades[clean_disc].append(round(float(grade), 1))
        return True

    def check_in_dormitory(self, dorm_number: int) -> bool:
        if not isinstance(dorm_number, int) or dorm_number < 1:
            return False
        self.dormitory_number = dorm_number
        return True

    def leave_dormitory(self) -> bool:
        if self.dormitory_number is None:
            return False
        self.dormitory_number = None
        return True

    def transfer_to_group(self, new_group_number: int) -> bool:
        if new_group_number == self.__group_number:
            return False
        self.group_number = new_group_number
        return True