class Faculty:
    def __init__(self, name, dean):
        self.name = name
        self.dean = dean
        self.__specialities = []
        self.__departments = []
        self.__building = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        clean = value.strip()
        if len(clean) < 3:
            raise ValueError("Name must have at least 3 characters")
        self.__name = clean

    @property
    def dean(self):
        return self.__dean

    @dean.setter
    def dean(self, value):
        if not isinstance(value, str):
            raise TypeError("Dean must be a string")
        clean = value.strip()
        if len(clean) < 5:
            raise ValueError("Dean name must have at least 5 characters")
        self.__dean = clean

    @property
    def specialities(self):
        return self.__specialities.copy()

    @property
    def departments(self):
        return self.__departments.copy()

    @property
    def building(self):
        return self.__building

    def add_speciality(self, speciality):
        from LR2.Speciality import Speciality
        if not isinstance(speciality, Speciality):
            raise TypeError("Speciality must be an instance of Speciality")
        if speciality not in self.__specialities:
            self.__specialities.append(speciality)
            if speciality.faculty_name != self.name:
                speciality.faculty_name = self.name
            return True
        return False

    def remove_speciality(self, speciality):
        if speciality in self.__specialities:
            self.__specialities.remove(speciality)
            return True
        return False

    def has_speciality(self, speciality):
        return speciality in self.__specialities

    def add_department(self, department):
        from LR2.Department import Department
        if not isinstance(department, Department):
            raise TypeError("Department must be an instance of Department")
        if department not in self.__departments:
            self.__departments.append(department)
            if department.faculty_name != self.name:
                department.faculty_name = self.name
            return True
        return False

    def remove_department(self, department):
        if department in self.__departments:
            self.__departments.remove(department)
            return True
        return False

    def has_department(self, department):
        return department in self.__departments

    def provide_dormitory(self, student, dormitory):
        from LR2.Student import Student
        from LR2.Dormitory import Dormitory

        if not isinstance(student, Student) or not isinstance(dormitory, Dormitory):
            raise TypeError("Invalid types for student or dormitory")
        if student.gpa <= 9.0:
            return False
        return dormitory.add_student(student)

    def open_department_in_building(self, department, building):
        from LR2.Department import Department
        from LR2.AcademyBuilding import AcademyBuilding

        if not isinstance(department, Department) or not isinstance(building, AcademyBuilding):
            raise TypeError("Invalid types for department or building")
        self.add_department(department)
        building.add_department(department)
        department.building = building
        return True

    def relocate_to_building(self, building):
        from LR2.AcademyBuilding import AcademyBuilding
        if not isinstance(building, AcademyBuilding):
            raise TypeError("Building must be an instance of AcademyBuilding")
        self.__building = building
        return True

    def get_total_students(self):
        total = 0
        for spec in self.__specialities:
            for group in spec.groups:
                total += len(group.students)
        return total

    def get_average_gpa(self):
        all_grades = []
        for spec in self.__specialities:
            for group in spec.groups:
                for student in group.students:
                    grades = student.get_grades()
                    for disc_grades in grades.values():
                        all_grades.extend(disc_grades)
        return round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    def __str__(self):
        return f"Факультет: {self.name} (декан: {self.dean})"