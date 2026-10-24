from LR1.AcademyBuilding import AcademyBuilding


class Staff:
    def __init__(self, name: str, age: int, salary: float, role: str):
        self.name = name
        self.age = age
        self.salary = salary
        self.role = role

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
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 18 or value > 100:
            raise ValueError("Age must be between 18 and 100")
        self.__age = value

    @property
    def salary(self) -> float:
        return self.__salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary must be positive")
        self.__salary = float(value)

    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise TypeError("Role must be a string")
        self.__role = value.strip().lower()

    def get_annual_salary(self) -> float:
        return round(self.salary * 12, 2)

    def increase_salary_if_short_staffed(self, building: AcademyBuilding, threshold: int = 5) -> bool:
        if not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Threshold must be a positive integer")

        if self.name in building.staff and len(building.staff) < threshold:
            self.salary = round(self.salary * 1.1, 2)
            return True
        return False

