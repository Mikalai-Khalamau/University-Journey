class Group:
    def __init__(self, number, speciality_name):
        self.number = number
        self.speciality_name = speciality_name
        self.__students = []
        self.__disciplines = []

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError("Number must be an integer")
        if value < 100000 or value > 999999:
            raise ValueError("Number must be a 6-digit integer")
        self.__number = value

    @property
    def speciality_name(self):
        return self.__speciality_name

    @speciality_name.setter
    def speciality_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Speciality name must be a string")
        self.__speciality_name = value.strip()

    @property
    def students(self):
        return self.__students.copy()

    @property
    def disciplines(self):
        return self.__disciplines.copy()

    def add_student(self, student):
        from LR2.Student import Student
        if not isinstance(student, Student):
            raise TypeError("Student must be an instance of Student")
        if student not in self.__students:
            self.__students.append(student)
            student.assign_to_group(self)
            for discipline in self.__disciplines:
                student.add_discipline(discipline)
            return True
        return False

    def remove_student(self, student):
        if student in self.__students:
            self.__students.remove(student)
            student.remove_from_group()
            return True
        return False

    def has_student(self, student):
        return student in self.__students

    def add_discipline(self, discipline):
        from LR2.Discipline import Discipline
        if not isinstance(discipline, Discipline):
            raise TypeError("Discipline must be an instance of Discipline")
        if discipline not in self.__disciplines:
            self.__disciplines.append(discipline)
            for student in self.__students:
                student.add_discipline(discipline)
            return True
        return False

    def remove_discipline(self, discipline):
        if discipline in self.__disciplines:
            self.__disciplines.remove(discipline)
            for student in self.__students:
                student.remove_discipline(discipline)
            return True
        return False

    def has_discipline(self, discipline):
        return discipline in self.__disciplines

    def get_average_gpa(self):
        if not self.__students:
            return 0.0
        total = sum(student.gpa for student in self.__students)
        return round(total / len(self.__students), 2)

    def get_students_count(self):
        return len(self.__students)

    def __str__(self):
        return f"Группа {self.number} ({self.speciality_name}), студентов: {len(self.__students)}"