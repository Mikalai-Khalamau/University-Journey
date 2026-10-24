from typing import List

class Department:
    def __init__(self, name: str, head: str):
        self.name = name
        self.head = head
        self.__teachers: List[str] = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Department name must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Department name must have at least 2 characters")
        self.__name = clean

    @property
    def head(self) -> str:
        return self.__head

    @head.setter
    def head(self, value):
        if not isinstance(value, str):
            raise TypeError("Department head must be a string")
        clean = value.strip()
        if len(clean) < 2:
            raise ValueError("Department head name must have at least 2 characters")
        self.__head = clean

    @property
    def teachers(self) -> List[str]:
        return self.__teachers.copy()

    def add_teacher(self, teacher_name: str) -> bool:
        clean = teacher_name.strip()
        if len(clean) < 2 or clean in self.__teachers:
            return False
        self.__teachers.append(clean)
        return True

    def remove_teacher(self, teacher_name: str) -> bool:
        clean = teacher_name.strip()
        if clean in self.__teachers:
            self.__teachers.remove(clean)
            return True
        return False

    def change_head(self, new_head_name: str) -> bool:
        clean = new_head_name.strip()
        if len(clean) < 2:
            return False
        self.head = clean
        return True

    def merge_with(self, other_department_name: str) -> str:
        return f"{self.name} + {other_department_name}"