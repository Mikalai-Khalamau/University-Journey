from LR2.Person import Person
class Student(Person):
    def __init__(self, name, passport_details, telephone_number, residence_place, course, education_form, gpa=0.0):
        super().__init__(name, passport_details, telephone_number)
        self.residence_place = residence_place
        self.course = course
        self.education_form = education_form
        self.gpa = gpa
        self.__disciplines = []
        self.__grades = {}
        self.__dormitory = None
        self.__group = None

    @property
    def residence_place(self):
        return self.__residence_place

    @residence_place.setter
    def residence_place(self, value):
        from LR2.ResidencePlace import ResidencePlace
        if not isinstance(value, ResidencePlace):
            raise TypeError("Residence place must be an instance of ResidencePlace")
        self.__residence_place = value

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, value):
        if not isinstance(value, int):
            raise TypeError("Course must be an integer")
        if value < 1 or value > 6:
            raise ValueError("Course must be between 1 and 6")
        self.__course = value

    @property
    def education_form(self):
        return self.__education_form

    @education_form.setter
    def education_form(self, value):
        if not isinstance(value, str):
            raise TypeError("Education form must be a string")
        clean = value.strip().capitalize()
        if clean not in ["Дневная", "Заочная"]:
            raise ValueError("Education form must be 'Дневная' or 'Заочная'")
        self.__education_form = clean

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("GPA must be a number")
        if value < 0.0 or value > 10.0:
            raise ValueError("GPA must be between 0.0 and 10.0")
        self.__gpa = round(float(value), 2)

    @property
    def disciplines(self):
        return self.__disciplines.copy()

    @property
    def dormitory(self):
        return self.__dormitory

    @property
    def group(self):
        return self.__group

    def assign_to_group(self, group):
        from LR2.Group import Group
        if not isinstance(group, Group):
            raise TypeError("Group must be an instance of Group")
        self.__group = group
        return True

    def remove_from_group(self):
        self.__group = None
        return True

    def add_discipline(self, discipline):
        from LR2.Discipline import Discipline
        if not isinstance(discipline, Discipline):
            raise TypeError("Discipline must be an instance of Discipline")
        if discipline not in self.__disciplines:
            self.__disciplines.append(discipline)
            return True
        return False

    def has_discipline(self, discipline):
        return discipline in self.__disciplines

    def add_grade(self, discipline, grade):
        if not isinstance(grade, (int, float)):
            raise TypeError("Grade must be a number")
        if not (1.0 <= grade <= 10.0):
            raise ValueError("Grade must be between 1.0 and 10.0")
        if discipline not in self.__disciplines:
            raise ValueError("Student is not enrolled in this discipline")

        if discipline not in self.__grades:
            self.__grades[discipline] = []
        self.__grades[discipline].append(round(float(grade), 1))
        self.__recalculate_gpa()
        return True

    def __recalculate_gpa(self):
        all_grades = [g for grades in self.__grades.values() for g in grades]
        self.gpa = round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    def get_grades(self):
        return {disc: grades.copy() for disc, grades in self.__grades.items()}

    def check_in_dormitory(self, dormitory):
        from LR2.Dormitory import Dormitory
        if not isinstance(dormitory, Dormitory):
            raise TypeError("Dormitory must be an instance of Dormitory")
        self.__dormitory = dormitory
        return True

    def leave_dormitory(self):
        if self.__dormitory is None:
            return False
        self.__dormitory = None
        return True

    def transfer_to_group(self, new_group):
        from LR2.Group import Group
        if not isinstance(new_group, Group):
            raise TypeError("Group must be an instance of Group")
        if self.__group:
            self.__group.remove_student(self)
        self.__group = new_group
        new_group.add_student(self)
        return True

    def get_role_description(self):
        return f"Студент {self.course} курса ({self.education_form} форма обучения)"

    def get_contact_info(self):
        dorm_info = f", общежитие {self.__dormitory.number}" if self.__dormitory else ""
        group_info = f", группа {self.__group.number}" if self.__group else ""
        return f"Студент: {self.name} | Тел: {self.telephone_number}{group_info}{dorm_info}"

    def remove_discipline(self, discipline):
        if discipline in self.__disciplines:
            self.__disciplines.remove(discipline)
            if discipline in self.__grades:
                del self.__grades[discipline]
            return True
        return False