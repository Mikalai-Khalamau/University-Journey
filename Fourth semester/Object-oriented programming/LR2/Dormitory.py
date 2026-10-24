from LR2.Building import Building

class Dormitory(Building):
    def __init__(self, name, address, number, capacity):
        super().__init__(name, address)
        self.number = number
        self.capacity = capacity
        self.__students = []
        self.__staff = []

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError("Number must be an integer")
        if value < 1 or value > 10:
            raise ValueError("Number must be between 1 and 10")
        self.__number = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value < 50 or value > 1000:
            raise ValueError("Capacity must be between 50 and 1000")
        self.__capacity = value

    @property
    def students(self):
        return self.__students.copy()

    @property
    def staff(self):
        return self.__staff.copy()

    def add_student(self, student):
        from LR2.Student import Student
        if not isinstance(student, Student):
            raise TypeError("Student must be an instance of Student")
        if len(self.__students) >= self.__capacity:
            return False
        if student not in self.__students:
            self.__students.append(student)
            student.check_in_dormitory(self)
            return True
        return False

    def remove_student(self, student):
        if student in self.__students:
            self.__students.remove(student)
            student.leave_dormitory()
            return True
        return False

    def has_student(self, student):
        return student in self.__students

    def add_staff(self, staff):
        from LR2.Staff import Staff
        if not isinstance(staff, Staff):
            raise TypeError("Staff must be an instance of Staff")
        if staff not in self.__staff:
            self.__staff.append(staff)
            staff.assign_to_dormitory(self)
            return True
        return False

    def remove_staff(self, staff):
        if staff in self.__staff:
            self.__staff.remove(staff)
            return True
        return False

    def has_staff(self, staff):
        return staff in self.__staff

    def expand_capacity(self, additional_places):
        if additional_places <= 0:
            return False
        self.__capacity += additional_places
        return True

    def get_occupancy_rate(self):
        if self.__capacity == 0:
            return 0.0
        return round(len(self.__students) / self.__capacity * 100, 1)

    def get_building_type(self):
        return "Общежитие"

    def get_occupancy_info(self):
        occupancy = self.get_occupancy_rate()
        return f"Заселено: {len(self.__students)}/{self.__capacity} ({occupancy}%)"

    def get_contact_info(self):
        return f"Общежитие {self.number}: {self.name} | Адрес: {self.address}"

    def __str__(self):
        return f"Общежитие {self.number} ({self.name})"

    def calculate_cost(self) -> float:
        base_cost = 8000.0
        student_cost = len(self.__students) * 300.0
        staff_cost = len(self.__staff) * 2000.0

        total = base_cost + student_cost + staff_cost
        return total