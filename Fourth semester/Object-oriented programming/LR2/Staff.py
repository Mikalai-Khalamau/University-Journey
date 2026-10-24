from LR2.Person import Person

class Staff(Person):
    def __init__(self, name, passport_details, telephone_number, salary, role):
        super().__init__(name, passport_details, telephone_number)
        self.salary = salary
        self.role = role
        self.__current_building = None
        self.__current_dormitory = None

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary must be positive")
        self.__salary = float(value)

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise TypeError("Role must be a string")
        self.__role = value.strip().capitalize()

    @property
    def current_building(self):
        return self.__current_building

    @property
    def current_dormitory(self):
        return self.__current_dormitory

    def assign_to_building(self, building):
        from LR2.AcademyBuilding import AcademyBuilding
        if not isinstance(building, AcademyBuilding):
            raise TypeError("Building must be an instance of AcademyBuilding")
        self.__current_building = building
        if building not in self.__current_building.staff:
            building.add_staff(self)
        return True

    def assign_to_dormitory(self, dormitory):
        from LR2.Dormitory import Dormitory
        if not isinstance(dormitory, Dormitory):
            raise TypeError("Dormitory must be an instance of Dormitory")
        self.__current_dormitory = dormitory
        if dormitory not in self.__current_dormitory.staff:
            dormitory.add_staff(self)
        return True

    def get_annual_salary(self):
        return round(self.salary * 12, 2)

    def increase_salary_if_short_staffed(self, building, threshold=5):
        if not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Threshold must be a positive integer")

        if building.is_understaffed(threshold):
            self.salary = round(self.salary * 1.1, 2)
            return True
        return False

    def get_role_description(self):
        location = ""
        if self.__current_building:
            location = f" (корпус {self.__current_building.number})"
        elif self.__current_dormitory:
            location = f" (общежитие {self.__current_dormitory.number})"
        return f"Сотрудник: {self.role}{location}, зарплата: {self.salary} BYN"

    def get_contact_info(self):
        location = ""
        if self.__current_building:
            location = f" | Корпус: {self.__current_building.name}"
        elif self.__current_dormitory:
            location = f" | Общежитие: {self.__current_dormitory.name}"
        return f"Сотрудник: {self.name} ({self.role}) | Тел: {self.telephone_number}{location}"