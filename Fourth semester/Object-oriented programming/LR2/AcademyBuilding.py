from LR2.Building import Building

class AcademyBuilding(Building):
    def __init__(self, name, address, number):
        super().__init__(name, address)
        self.number = number
        self.__departments = []
        self.__staff = []

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError("Number must be an integer")
        if value < 1 or value > 20:
            raise ValueError("Number must be between 1 and 20")
        self.__number = value

    @property
    def departments(self):
        return self.__departments.copy()

    @property
    def staff(self):
        return self.__staff.copy()

    def add_department(self, department):
        from LR2.Department import Department
        if not isinstance(department, Department):
            raise TypeError("Department must be an instance of Department")
        if department not in self.__departments:
            self.__departments.append(department)
            if hasattr(department, 'building') and department.building is None:
                department.building = self
            return True
        return False

    def remove_department(self, department):
        if department in self.__departments:
            self.__departments.remove(department)
            return True
        return False

    def has_department(self, department):
        return department in self.__departments

    def add_staff(self, staff):
        from LR2.Staff import Staff
        if not isinstance(staff, Staff):
            raise TypeError("Staff must be an instance of Staff")
        if staff not in self.__staff:
            self.__staff.append(staff)
            staff.assign_to_building(self)
            return True
        return False

    def remove_staff(self, staff):
        if staff in self.__staff:
            self.__staff.remove(staff)
            return True
        return False

    def has_staff(self, staff):
        return staff in self.__staff

    def is_understaffed(self, threshold = 5):
        if not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Threshold must be a positive integer")
        return len(self.__staff) < threshold

    def dismiss_all_staff(self):
        count = len(self.__staff)
        self.__staff.clear()
        return count

    def get_building_type(self):
        return "Учебный корпус"

    def get_occupancy_info(self):
        dept_count = len(self.__departments)
        staff_count = len(self.__staff)
        return f"Кафедр: {dept_count}, Сотрудников: {staff_count}"

    def get_contact_info(self):
        return f"Корпус {self.number}: {self.name} | Адрес: {self.address}"

    def __str__(self):
        return f"Корпус {self.number} ({self.name})"

    def calculate_cost(self) -> float:
        base_cost = 10000.0
        department_cost = len(self.__departments) * 5000.0
        staff_cost = len(self.__staff) * 2000.0
        total = base_cost + department_cost + staff_cost
        return total
