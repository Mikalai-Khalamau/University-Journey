class Discipline:
    def __init__(self, name, hours):
        self.name = name
        self.hours = hours
        self.__teachers = []

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
    def hours(self):
        return self.__hours

    @hours.setter
    def hours(self, value):
        if not isinstance(value, int):
            raise TypeError("Hours must be an integer")
        if value < 16 or value > 300:
            raise ValueError("Hours must be between 16 and 300")
        self.__hours = value

    @property
    def teachers(self):
        return self.__teachers.copy()

    def add_teacher(self, teacher):
        from LR2.Teacher import Teacher
        if not isinstance(teacher, Teacher):
            raise TypeError("Teacher must be an instance of Teacher")
        if teacher not in self.__teachers:
            self.__teachers.append(teacher)
            return True
        return False

    def remove_teacher(self, teacher):
        if teacher in self.__teachers:
            self.__teachers.remove(teacher)
            return True
        return False

    def has_teacher(self, teacher):
        return teacher in self.__teachers

    def assign_teacher(self, teacher):
        return self.add_teacher(teacher)

    def is_heavyload(self):
        return self.hours > 100

    def get_weekly_hours(self):
        return round(self.hours / 18, 1)

    def __str__(self):
        return f"Дисциплина: {self.name} ({self.hours} ч.)"