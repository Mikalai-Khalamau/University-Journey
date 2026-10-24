class Department:
    def __init__(self, name, head = "", faculty_name = ""):
        self.name = name
        self.head = head
        self.faculty_name = faculty_name
        self.__teachers = []
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
    def head(self):
        return self.__head

    @head.setter
    def head(self, value):
        if not isinstance(value, str):
            raise TypeError("Head must be a string")
        self.__head = value.strip()

    @property
    def faculty_name(self):
        return self.__faculty_name

    @faculty_name.setter
    def faculty_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Faculty name must be a string")
        self.__faculty_name = value.strip()

    @property
    def teachers(self):
        return self.__teachers.copy()

    @property
    def building(self):
        return self.__building

    @building.setter
    def building(self, value):
        from LR2.AcademyBuilding import AcademyBuilding
        if value is not None and not isinstance(value, AcademyBuilding):
            raise TypeError("Building must be an instance of AcademyBuilding")
        self.__building = value

    def add_teacher(self, teacher):
        from LR2.Teacher import Teacher
        if not isinstance(teacher, Teacher):
            raise TypeError("Teacher must be an instance of Teacher")
        if teacher not in self.__teachers:
            self.__teachers.append(teacher)
            if teacher.department != self:
                teacher.department = self
            return True
        return False

    def remove_teacher(self, teacher):
        if teacher in self.__teachers:
            self.__teachers.remove(teacher)
            return True
        return False

    def has_teacher(self, teacher):
        return teacher in self.__teachers

    def change_head(self, new_head_name):
        clean = new_head_name.strip()
        if len(clean) < 5:
            return False
        self.head = clean
        return True

    def merge_with(self, other_department):
        if not isinstance(other_department, Department):
            raise TypeError("Other department must be an instance of Department")
        return f"{self.name} + {other_department.name}"

    def get_teacher_count_by_rank(self, rank):
        return sum(1 for t in self.__teachers if t.academic_rank == rank)

    def __str__(self):
        return f"Кафедра: {self.name} (заведующий: {self.head})"