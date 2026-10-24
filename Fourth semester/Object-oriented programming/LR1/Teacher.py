from typing import List
from LR1.Student import Student

class Teacher:
    VALID_RANKS = ["ассистент", "преподаватель", "старший преподаватель", "доцент", "профессор"]

    def __init__(self, name: str, age: int, academic_rank: str, department: str):
        self.name = name
        self.age = age
        self.academic_rank = academic_rank
        self.department = department
        self.__disciplines: List[str] = []

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
        if value < 18 or value > 100:
            raise ValueError("Age must be between 18 and 100")
        self.__age = value

    @property
    def academic_rank(self) -> str:
        return self.__academic_rank

    @academic_rank.setter
    def academic_rank(self, value):
        if not isinstance(value, str):
            raise TypeError("Academic rank must be a string")
        clean = value.strip().lower()
        if clean not in self.VALID_RANKS:
            raise ValueError(f"Rank must be one of: {', '.join(self.VALID_RANKS)}")
        self.__academic_rank = clean

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value):
        if not isinstance(value, str):
            raise TypeError("Department must be a string")
        self.__department = value.strip()

    @property
    def disciplines(self) -> List[str]:
        return self.__disciplines.copy()

    def assign_discipline(self, discipline: str) -> bool:
        clean = discipline.strip()
        if not clean:
            raise ValueError("Discipline name cannot be empty")
        if clean not in self.__disciplines:
            self.__disciplines.append(clean)
            return True
        return False

    def grade_student(self, student: Student, discipline: str, grade: float) -> bool:
        clean_disc = discipline.strip()
        if clean_disc not in self.__disciplines:
            return False
        return student.add_grade(clean_disc, grade)