from LR1.Student import Student
from LR1.Teacher import Teacher

class Rectorate:
    def __init__(self, rector: str):
        self.rector = rector
        self.__vice_rectors: list = []
        self.__scholarships_awarded: int = 0
        self.__bonuses_awarded: int = 0

    @property
    def rector(self) -> str:
        return self.__rector

    @rector.setter
    def rector(self, value):
        if not isinstance(value, str):
            raise TypeError("Rector must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Rector name must have at least 2 characters")
        self.__rector = clean

    @property
    def vice_rectors(self) -> list:
        return self.__vice_rectors.copy()

    @property
    def scholarships_awarded(self) -> int:
        return self.__scholarships_awarded

    @property
    def bonuses_awarded(self) -> int:
        return self.__bonuses_awarded

    def appoint_vice_rector(self, vice_rector: str) -> bool:
        clean = vice_rector.strip()
        if len(clean) < 2 or clean in self.__vice_rectors:
            return False
        self.__vice_rectors.append(clean)
        return True

    def dismiss_vice_rector(self, vice_rector: str) -> bool:
        clean = vice_rector.strip()
        if clean in self.__vice_rectors:
            self.__vice_rectors.remove(clean)
            return True
        return False

    def award_scholarship(self, student: Student) -> bool:
        if student.gpa > 6.0:
            self.__scholarships_awarded += 1
            return True
        return False

    def award_bonus(self, teacher: Teacher) -> bool:
        if len(teacher.disciplines) > 6:
            self.__bonuses_awarded += 1
            return True
        return False
