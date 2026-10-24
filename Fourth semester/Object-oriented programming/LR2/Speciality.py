class Speciality:
    def __init__(self, name, duration_years, faculty_name=""):
        self.name = name
        self.duration_years = duration_years
        self.faculty_name = faculty_name
        self.__groups = []

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
    def duration_years(self):
        return self.__duration_years

    @duration_years.setter
    def duration_years(self, value):
        if not isinstance(value, int):
            raise TypeError("Duration must be an integer")
        if value < 4 or value > 6:
            raise ValueError("Duration must be between 4 and 6 years")
        self.__duration_years = value

    @property
    def faculty_name(self):
        return self.__faculty_name

    @faculty_name.setter
    def faculty_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Faculty name must be a string")
        self.__faculty_name = value.strip()

    @property
    def groups(self):
        return self.__groups.copy()

    def add_group(self, group):
        from LR2.Group import Group
        if not isinstance(group, Group):
            raise TypeError("Group must be an instance of Group")
        if group not in self.__groups:
            self.__groups.append(group)
            if group.speciality_name != self.name:
                group.speciality_name = self.name
            return True
        return False

    def remove_group(self, group):
        if group in self.__groups:
            self.__groups.remove(group)
            return True
        return False

    def has_group(self, group):
        return group in self.__groups

    def add_disciplines_to_group(self, group, disciplines):
        from LR2.Group import Group
        from LR2.Discipline import Discipline

        if not isinstance(group, Group):
            raise TypeError("Group must be an instance of Group")
        if not isinstance(disciplines, list):
            raise TypeError("Disciplines must be a list")

        if group not in self.__groups:
            return 0

        added = 0
        for discipline in disciplines:
            if isinstance(discipline, Discipline) and group.add_discipline(discipline):
                added += 1
        return added

    def get_total_students(self):
        return sum(len(group.students) for group in self.__groups)

    def __str__(self):
        return f"Специальность: {self.name} ({self.duration_years} года)"