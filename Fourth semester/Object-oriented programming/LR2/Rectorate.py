
class Rectorate:
    def __init__(self, rector):
        self.rector = rector
        self.__vice_rectors = []
        self.__scholarships_awarded = 0
        self.__bonuses_awarded = 0
        self.__name = "Ректорат"
        self.__universities = []
        self.__staff = []

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
    def rector(self):
        return self.__rector

    @rector.setter
    def rector(self, value):
        if not isinstance(value, str):
            raise TypeError("Rector must be a string")
        clean = value.strip()
        if len(clean) < 5:
            raise ValueError("Rector name must have at least 5 characters")
        self.__rector = clean

    @property
    def vice_rectors(self):
        return self.__vice_rectors.copy()

    @property
    def scholarships_awarded(self):
        return self.__scholarships_awarded

    @property
    def bonuses_awarded(self):
        return self.__bonuses_awarded

    @property
    def universities(self):
        return self.__universities.copy()

    @property
    def staff(self):
        return self.__staff.copy()

    def appoint_vice_rector(self, vice_rector):
        clean = vice_rector.strip()
        if len(clean) < 5 or clean in self.__vice_rectors:
            return False
        self.__vice_rectors.append(clean)
        return True

    def dismiss_vice_rector(self, vice_rector):
        clean = vice_rector.strip()
        if clean in self.__vice_rectors:
            self.__vice_rectors.remove(clean)
            return True
        return False

    def add_university(self, university):
        if university not in self.__universities:
            self.__universities.append(university)
            return True
        return False

    def remove_university(self, university):
        if university in self.__universities:
            self.__universities.remove(university)
            return True
        return False

    def add_staff(self, staff_member):
        if staff_member not in self.__staff:
            self.__staff.append(staff_member)
            return True
        return False

    def remove_staff(self, staff_member):
        if staff_member in self.__staff:
            self.__staff.remove(staff_member)
            return True
        return False

    def get_all_university_buildings(self):
        all_buildings = []
        for uni in self.__universities:
            all_buildings.extend(uni.buildings)
        return all_buildings

    def get_all_university_staff(self):
        all_staff = []
        for uni in self.__universities:
            all_staff.extend(uni.staff)
        return all_staff

    def get_total_students(self):
        total = 0
        for uni in self.__universities:
            total += uni.get_total_students()
        return total

    def consolidate_dormitories(self):
        report = {}
        for uni in self.__universities:
            for building in uni.buildings:
                from LR2.Dormitory import Dormitory
                if isinstance(building, Dormitory):
                    report[building] = building.get_occupancy_rate()
        return report

    def award(self, entity):
        """Метод для награждения разных типов сущностей"""
        from LR2.Student import Student
        from LR2.Teacher import Teacher
        from LR2.Staff import Staff

        if isinstance(entity, Student):
            if entity.gpa > 6.0:
                self.__scholarships_awarded += 1
                return f"Студент {entity.name} получил стипендию. GPA: {entity.gpa}"
            return f"Студент {entity.name} не прошёл по баллам (требуется GPA > 6.0)"

        elif isinstance(entity, Teacher):
            if len(entity.disciplines) > 6:
                self.__bonuses_awarded += 1
                return f"Преподаватель {entity.name} получил премию. Дисциплин: {len(entity.disciplines)}"
            return f"Преподаватель {entity.name} не прошёл по количеству дисциплин (требуется > 6)"

        elif isinstance(entity, Staff):
            original_salary = entity.salary
            entity.salary = round(entity.salary * 1.15, 2)
            self.__bonuses_awarded += 1
            return f"Сотрудник {entity.name} получил премию. Зарплата: {original_salary} → {entity.salary} BYN"

        else:
            raise NotImplementedError(f"Невозможно наградить сущность типа {type(entity).__name__}")

    def generate_report(self):
        report = f"Ректор: {self.rector}\n"
        report += f"Проректоры: {len(self.__vice_rectors)} ({', '.join(self.__vice_rectors) if self.__vice_rectors else 'нет'})\n"
        report += f"Университетов в подчинении: {len(self.__universities)}\n"
        report += f"Сотрудников ректората: {len(self.__staff)}\n"
        report += f"Выдано стипендий: {self.__scholarships_awarded}\n"
        report += f"Выдано премий: {self.__bonuses_awarded}\n"

        if self.__universities:
            total_students = self.get_total_students()
            report += f"Всего студентов в университетах: {total_students}\n"

        report += "=" * 70
        return report

    def __str__(self):
        return f"Ректорат (ректор: {self.rector}, проректоров: {len(self.__vice_rectors)})"