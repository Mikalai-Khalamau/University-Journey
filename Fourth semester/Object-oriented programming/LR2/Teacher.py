from LR2.Person import Person
from LR2.AcademicRank import AcademicRank

class Teacher(Person):
    def __init__(self, name, passport_details, telephone_number, academic_rank):
        super().__init__(name, passport_details, telephone_number)
        self.academic_rank = academic_rank
        self.__disciplines = []
        self.__department = None

    @property
    def academic_rank(self):
        return self.__academic_rank

    @academic_rank.setter
    def academic_rank(self, value):
        if not isinstance(value, AcademicRank):
            raise TypeError("Academic rank must be an instance of AcademicRank")
        self.__academic_rank = value

    @property
    def disciplines(self):
        return self.__disciplines.copy()

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        from LR2.Department import Department
        if value is not None and not isinstance(value, Department):
            raise TypeError("Department must be an instance of Department")
        self.__department = value

    def add_discipline(self, discipline):
        from LR2.Discipline import Discipline
        if not isinstance(discipline, Discipline):
            raise TypeError("Discipline must be an instance of Discipline")
        if discipline not in self.__disciplines:
            self.__disciplines.append(discipline)
            discipline.add_teacher(self)
            return True
        return False

    def remove_discipline(self, discipline):
        if discipline in self.__disciplines:
            self.__disciplines.remove(discipline)
            discipline.remove_teacher(self)
            return True
        return False

    def has_discipline(self, discipline):
        return discipline in self.__disciplines

    def grade_student(self, student, discipline, grade):
        if discipline not in self.__disciplines:
            return False
        return student.add_grade(discipline, grade)

    def promote_student(self, student):
        if 1 <= student.course < 6:
            student.course += 1
            return True
        return False

    def assign_to_department(self, department):
        from LR2.Department import Department
        if not isinstance(department, Department):
            raise TypeError("Department must be an instance of Department")
        self.__department = department
        department.add_teacher(self)
        return True

    def get_role_description(self):
        dept_info = f", кафедра {self.__department.name}" if self.__department else ""
        return f"Преподаватель ({self.academic_rank.value}), дисциплин: {len(self.__disciplines)}{dept_info}"

    def get_contact_info(self):
        dept_info = f" | Кафедра: {self.__department.name}" if self.__department else ""
        return f"Преподаватель: {self.name} | Тел: {self.telephone_number}{dept_info}"