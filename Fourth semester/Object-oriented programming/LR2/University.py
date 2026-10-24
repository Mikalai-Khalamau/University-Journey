from typing import TypeVar, List, Callable

from LR2.AcademyBuilding import AcademyBuilding
from LR2.Building import Building
from LR2.Dormitory import Dormitory
from LR2.Student import Student
from LR2.Teacher import Teacher
from LR2.Staff import Staff

T = TypeVar('T')

class University:
    def __init__(self, name, rectorate):
        self.name = name
        self.rectorate = rectorate
        self.__faculties = []
        self.__buildings = []
        self.__dormitories = []

    def find_in_collection(self, items: List[T], predicate: Callable[[T], bool]):
        return [item for item in items if predicate(item)]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("University name must be a string")
        clean = value.strip()
        if len(clean) < 5:
            raise ValueError("University name must have at least 5 characters")
        self.__name = clean

    @property
    def faculties(self):
        return self.__faculties.copy()

    @property
    def buildings(self):
        return self.__buildings.copy()

    @property
    def dormitories(self):
        return self.__dormitories.copy()

    def add_faculty(self, faculty):
        if faculty not in self.__faculties:
            self.__faculties.append(faculty)
            return True
        return False

    def add_building(self, building):
        if building not in self.__buildings:
            self.__buildings.append(building)
            return True
        return False

    def add_dormitory(self, dormitory):
        if dormitory not in self.__dormitories:
            self.__dormitories.append(dormitory)
            return True
        return False

    def find_entities_by_type(self, entity_type):
        results = []

        if issubclass(entity_type, Student):
            for faculty in self.__faculties:
                for spec in faculty.specialities:
                    for group in spec.groups:
                        results.extend([s for s in group.students if isinstance(s, entity_type)])

        if issubclass(entity_type, Teacher):
            teachers_set = set()
            for faculty in self.__faculties:
                for dept in faculty.departments:
                    teachers_set.update([t for t in dept.teachers if isinstance(t, entity_type)])
            results.extend(teachers_set)

        if issubclass(entity_type, Staff):
            staff_set = set()
            for building in self.__buildings:
                staff_set.update([s for s in building.staff if isinstance(s, entity_type)])
            for dorm in self.__dormitories:
                staff_set.update([s for s in dorm.staff if isinstance(s, entity_type)])
            results.extend(staff_set)

        if issubclass(entity_type, AcademyBuilding):
            results.extend([b for b in self.__buildings if isinstance(b, entity_type)])
        if issubclass(entity_type, Dormitory):
            results.extend([d for d in self.__dormitories if isinstance(d, entity_type)])

        if issubclass(entity_type, self.__faculties[0].__class__) if self.__faculties else False:
            results.extend([f for f in self.__faculties if isinstance(f, entity_type)])

        return results

    def filter_entities(self, entity_type, predicate):
        all_entities = self.find_entities_by_type(entity_type)
        return [entity for entity in all_entities if predicate(entity)]

    def get_total_students(self):
        return sum(faculty.get_total_students() for faculty in self.__faculties)

    def get_total_staff(self):
        staff_count = 0
        for building in self.__buildings:
            staff_count += len(building.staff)
        for dorm in self.__dormitories:
            staff_count += len(dorm.staff)
        return staff_count

    def get_average_gpa(self):
        all_grades = []
        for faculty in self.__faculties:
            for spec in faculty.specialities:
                for group in spec.groups:
                    for student in group.students:
                        grades = student.get_grades()
                        for disc_grades in grades.values():
                            all_grades.extend(disc_grades)
        return round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    def generate_university_report(self):
        report = f"Ректорат: {self.rectorate.rector}\n"
        report += f"Факультетов: {len(self.__faculties)}\n"
        report += f"Учебных корпусов: {len(self.__buildings)}\n"
        report += f"Общежитий: {len(self.__dormitories)}\n"
        report += f"Всего студентов: {self.get_total_students()}\n"
        report += f"Всего сотрудников: {self.get_total_staff()}\n"
        report += f"Средний GPA по университету: {self.get_average_gpa()}\n"
        report += f"Выдано стипендий: {self.rectorate.scholarships_awarded}\n"
        report += f"Выдано премий: {self.rectorate.bonuses_awarded}\n"
        return report

    def __str__(self):
        return f"Университет: {self.name} | Факультетов: {len(self.__faculties)}"

    def print_building_info(self, building: Building) :
        info = f"Здание: {building.name}\n"
        return info