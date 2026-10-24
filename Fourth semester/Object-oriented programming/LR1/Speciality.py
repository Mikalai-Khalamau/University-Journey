from typing import List
from LR1.Group import Group


class Speciality:
    def __init__(self, name: str, duration_years: int, faculty: str):
        self.name = name
        self.duration_years = duration_years
        self.faculty = faculty
        self.__groups: List[int] = []

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
    def duration_years(self) -> int:
        return self.__duration_years

    @duration_years.setter
    def duration_years(self, value):
        if not isinstance(value, int):
            raise TypeError("Duration must be an integer")
        if value < 4 or value > 6:
            raise ValueError("Duration must be between 4 and 6 years")
        self.__duration_years = value

    @property
    def faculty(self) -> str:
        return self.__faculty

    @faculty.setter
    def faculty(self, value):
        if not isinstance(value, str):
            raise TypeError("Faculty must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Faculty name must have at least 2 characters")
        self.__faculty = clean

    @property
    def groups(self) -> List[int]:
        return self.__groups.copy()

    def add_group(self, group_number) -> bool:
        if not isinstance(group_number, int):
            return False
        if group_number not in self.__groups:
            self.__groups.append(group_number)
            return True
        return False

    def remove_group(self, group_number: int) -> bool:
        if group_number in self.__groups:
            self.__groups.remove(group_number)
            return True
        return False

    def add_disciplines_to_group(self, group: Group, disciplines: List[str]) -> int:
        if group.speciality != self.name:
            return 0

        added = 0
        for discipline in disciplines:
            clean_disc = discipline.strip()
            if clean_disc and group.add_discipline(clean_disc):
                added += 1
        return added