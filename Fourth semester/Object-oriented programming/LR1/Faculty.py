from typing import List
from LR1.Student import Student
from LR1.Dormitory import Dormitory
from LR1.AcademyBuilding import AcademyBuilding

class Faculty:
    def __init__(self, name: str, dean: str):
        self.name = name
        self.dean = dean
        self.__specialities: List[str] = []
        self.__departments: List[str] = []
        self.building_number: int

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
    def dean(self) -> str:
        return self.__dean

    @dean.setter
    def dean(self, value):
        if not isinstance(value, str):
            raise TypeError("Dean must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Dean name must have at least 2 characters")
        self.__dean = clean

    @property
    def specialities(self) -> List[str]:
        return self.__specialities.copy()

    @property
    def departments(self) -> List[str]:
        return self.__departments.copy()

    def add_speciality(self, speciality_name: str) -> bool:
        clean = speciality_name.strip()
        if len(clean) < 2 or clean in self.__specialities:
            return False
        self.__specialities.append(clean)
        return True

    def remove_speciality(self, speciality_name: str) -> bool:
        clean = speciality_name.strip()
        if clean in self.__specialities:
            self.__specialities.remove(clean)
            return True
        return False

    def provide_dormitory(self, student: Student, dormitory: Dormitory) -> bool:
        if student.gpa <= 9.0:
            return False
        if dormitory.add_student(student.name):
            student.check_in_dormitory(dormitory.number)
            return True
        return False

    def open_department_in_building(self, department_name: str, building: AcademyBuilding) -> bool:
        clean_name = department_name.strip()
        if len(clean_name) < 2:
            return False
        if clean_name not in self.__departments:
            self.__departments.append(clean_name)
        building.add_department(clean_name)
        return True

    def relocate_to_building(self, building: AcademyBuilding) -> bool:
        self.building_number = building.number
        return True