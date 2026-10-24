from LR1.AcademyBuilding import AcademyBuilding
from LR1.Department import Department
from LR1.Discipline import Discipline
from LR1.Dormitory import Dormitory
from LR1.Faculty import Faculty
from LR1.Group import Group
from LR1.Rectorate import Rectorate
from LR1.Speciality import Speciality
from LR1.Staff import Staff
from LR1.Student import Student
from LR1.Teacher import Teacher


def main():
    print("Демонстрационный сценарий БГУИР")

    print("\n[1] Создание учебных корпусов и общежитий")
    building_2 = AcademyBuilding("Корпус 2", "ул. Петруся Бровки, 4", "+375 (17) 293-21-71", 2)
    building_1 = AcademyBuilding("Корпус 1", "ул. Петруся Бровки, 6", "+375 (17) 293-88-55", 1)
    building_3 = AcademyBuilding("Корпус 3", "ул. Петруся Бровки, 8", "+375 (17) 293-15-90", 3)
    dormitory_4 = Dormitory("Общежитие 4", "пр. Дзержинского, 95", "+375 (29) 123-45-67", 4, 1000)
    dormitory_5 = Dormitory("Общежитие 5", "ул. Семашко, 10", "+375 (44) 987-65-43", 5, 1500)

    print("Созданы учебные корпуса:")
    print(f"  - {building_2.name} ({building_2.address})")
    print(f"  - {building_1.name} ({building_1.address})")
    print(f"  - {building_3.name} ({building_3.address})")
    print("Созданы общежития:")
    print(f"  - {dormitory_4.name} ({dormitory_4.address}, вместимость: {dormitory_4.capacity})")
    print(f"  - {dormitory_5.name} ({dormitory_5.address}, вместимость: {dormitory_5.capacity})")

    print("\n[2] Создание администрации")
    rectorate = Rectorate("Богуш В.А.")
    rectorate.appoint_vice_rector("Шнейдеров В.В.")
    rectorate.appoint_vice_rector("Кузнецов С.С.")

    fksis = Faculty("ФКСиС", "Ульянов Н.И.")
    fkp = Faculty("ФКП", "Козлов Г.Д.")
    fitu = Faculty("ФИТУ", "Новиков Д.Е.")

    fksis.relocate_to_building(building_2)
    fkp.relocate_to_building(building_1)
    fitu.relocate_to_building(building_3)

    print(f"Ректорат: {rectorate.rector}")
    print("Факультеты:")
    print(f"  - {fksis.name} (декан: {fksis.dean}, корпус {fksis.building_number})")
    print(f"  - {fkp.name} (декан: {fkp.dean}, корпус {fkp.building_number})")
    print(f"  - {fitu.name} (декан: {fitu.dean}, корпус {fitu.building_number})")

    print("\n[3] Создание кафедр")
    dept_informatics = Department("Кафедра информатики", "Сиротко А.А.")
    dept_poit = Department("Кафедра ПОИТ", "Соколов Ж.З.")
    dept_math = Department("Кафедра высшей математики", "Орлов З.И.")

    fksis.open_department_in_building(dept_informatics.name, building_2)
    fkp.open_department_in_building(dept_poit.name, building_1)
    fitu.open_department_in_building(dept_math.name, building_3)

    print("Кафедры:")
    print(f"  - {dept_informatics.name} ({dept_informatics.head})")
    print(f"  - {dept_poit.name} ({dept_poit.head})")
    print(f"  - {dept_math.name} ({dept_math.head})")

    print("\n[4] Создание преподавателей")
    teacher_siroko = Teacher("Сиротко А.А.", 52, "профессор", dept_informatics.name)
    teacher_sokolov = Teacher("Соколов Ж.З.", 48, "доцент", dept_poit.name)
    teacher_orlov = Teacher("Орлов З.И.", 60, "профессор", dept_math.name)

    dept_informatics.add_teacher(teacher_siroko.name)
    dept_poit.add_teacher(teacher_sokolov.name)
    dept_math.add_teacher(teacher_orlov.name)

    print("Преподаватели:")
    print(f"  - {teacher_siroko.name} ({teacher_siroko.academic_rank}, {teacher_siroko.department})")
    print(f"  - {teacher_sokolov.name} ({teacher_sokolov.academic_rank}, {teacher_sokolov.department})")
    print(f"  - {teacher_orlov.name} ({teacher_orlov.academic_rank}, {teacher_orlov.department})")

    # 5. Создание дисциплин
    print("\n[5] Создание дисциплин")
    programming = Discipline("Программирование", 180)
    databases = Discipline("Базы данных", 144)
    math_analysis = Discipline("Математический анализ", 216)

    programming.assign_teacher(teacher_siroko)
    databases.assign_teacher(teacher_sokolov)
    math_analysis.assign_teacher(teacher_orlov)

    teacher_siroko.assign_discipline(programming.name)
    teacher_sokolov.assign_discipline(databases.name)
    teacher_orlov.assign_discipline(math_analysis.name)

    print("Дисциплины:")
    print(f"  - {programming.name} ({programming.hours} ч., преподаватели: {', '.join(programming.teachers)})")
    print(f"  - {databases.name} ({databases.hours} ч., преподаватели: {', '.join(databases.teachers)})")
    print(f"  - {math_analysis.name} ({math_analysis.hours} ч., преподаватели: {', '.join(math_analysis.teachers)})")

    print("\n[6] Создание специальностей и групп")
    spec_iitp = Speciality("IITP", 4, fksis.name)
    spec_pois = Speciality("POIT", 4, fkp.name)
    spec_vm = Speciality("VM", 4, fitu.name)

    fksis.add_speciality(spec_iitp.name)
    fkp.add_speciality(spec_pois.name)
    fitu.add_speciality(spec_vm.name)

    group_453503 = Group(453503, spec_iitp.name)
    group_451501 = Group(451501, spec_pois.name)
    group_450505 = Group(450505, spec_vm.name)

    spec_iitp.add_group(group_453503.number)
    spec_pois.add_group(group_451501.number)
    spec_vm.add_group(group_450505.number)

    print("Специальности:")
    print(f"  - {spec_iitp.name} ({spec_iitp.duration_years} года, факультет: {spec_iitp.faculty})")
    print(f"  - {spec_pois.name} ({spec_pois.duration_years} года, факультет: {spec_pois.faculty})")
    print(f"  - {spec_vm.name} ({spec_vm.duration_years} года, факультет: {spec_vm.faculty})")
    print("Группы:")
    print(f"  - Группа {group_453503.number} ({group_453503.speciality})")
    print(f"  - Группа {group_451501.number} ({group_451501.speciality})")
    print(f"  - Группа {group_450505.number} ({group_450505.speciality})")

    print("\n[7] Создание студентов")
    student_ivanov = Student("Иванов А.А.", 18, 1, group_453503.number)
    student_petrov = Student("Петров Б.Б.", 19, 1, group_453503.number)
    student_sidorov = Student("Сидоров В.В.", 18, 1, group_451501.number)
    student_kuznetsov = Student("Кузнецов Г.Г.", 18, 1, group_450505.number)

    group_453503.add_student(student_ivanov.name)
    group_453503.add_student(student_petrov.name)
    group_451501.add_student(student_sidorov.name)
    group_450505.add_student(student_kuznetsov.name)

    print("Студенты:")
    print(f"  - {student_ivanov.name} (группа {student_ivanov.group_number}, курс {student_ivanov.course})")
    print(f"  - {student_petrov.name} (группа {student_petrov.group_number}, курс {student_petrov.course})")
    print(f"  - {student_sidorov.name} (группа {student_sidorov.group_number}, курс {student_sidorov.course})")
    print(f"  - {student_kuznetsov.name} (группа {student_kuznetsov.group_number}, курс {student_kuznetsov.course})")

    print("\n[8] Учебный процесс: выставление оценок")
    teacher_siroko.grade_student(student_ivanov, programming.name, 8.0)
    teacher_siroko.grade_student(student_ivanov, programming.name, 10.0)
    teacher_sokolov.grade_student(student_sidorov, databases.name, 7)
    teacher_orlov.grade_student(student_kuznetsov, math_analysis.name, 9)

    print(f"Оценки студента {student_ivanov.name}: GPA = {student_ivanov.gpa}")
    print(f"Оценки студента {student_kuznetsov.name}: GPA = {student_kuznetsov.gpa}")

    print("\n[9] Специальность добавляет дисциплины группе")
    disciplines = [programming.name, databases.name, math_analysis.name]
    added = spec_iitp.add_disciplines_to_group(group_453503, disciplines)
    print(f"Добавлено дисциплин в группу {group_453503.number}: {added}")
    print(f"Дисциплины группы: {', '.join(group_453503.disciplines)}")

    print("\n[10] Ректорат выдает стипендии (GPA > 6.0)")
    awarded = 0
    if rectorate.award_scholarship(student_ivanov):
        print(f"Студент {student_ivanov.name} получил стипендию (GPA: {student_ivanov.gpa})")
        awarded += 1
    if rectorate.award_scholarship(student_kuznetsov):
        print(f"Студент {student_kuznetsov.name} получил стипендию (GPA: {student_kuznetsov.gpa})")
        awarded += 1
    if not rectorate.award_scholarship(student_sidorov):
        print(f"Студент {student_sidorov.name} не получил стипендию (GPA: {student_sidorov.gpa})")
    print(f"Всего выдано стипендий: {awarded}")

    print("\n[11] Ректорат выдает премии преподавателям (дисциплин > 6)")
    for i in range(7):
        teacher_siroko.assign_discipline(f"Доп_дисциплина_{i + 1}")

    if rectorate.award_bonus(teacher_siroko):
        print(f"Преподаватель {teacher_siroko.name} получил премию ({len(teacher_siroko.disciplines)} дисциплин)")
    if not rectorate.award_bonus(teacher_sokolov):
        print(f"Преподаватель {teacher_sokolov.name} не получил премию ({len(teacher_sokolov.disciplines)} дисциплин)")
    print(f"Всего выдано премий: {rectorate.bonuses_awarded}")

    print("\n[12] Факультет предоставляет общежитие (GPA > 9.0)")
    if fksis.provide_dormitory(student_ivanov, dormitory_4):
        print(f"Студент {student_ivanov.name} заселен в {dormitory_4.name} (корпус: {student_ivanov.dormitory_number})")
    else:
        print(f"Студент {student_ivanov.name} не прошел по баллам (требуется GPA > 9.0)")

    if not fkp.provide_dormitory(student_sidorov, dormitory_5):
        print(f"Студент {student_sidorov.name} не прошел по баллам (GPA: {student_sidorov.gpa})")

    print(f"Студенты в общежитии 4: {len(dormitory_4.students)}")
    print(f"Студенты в общежитии 5: {len(dormitory_5.students)}")

    print("\n[13] Работа сотрудников")
    janitor = Staff("Ковалев И.К.", 42, 1500.0, "Уборщик")
    security = Staff("Михайлов П.М.", 35, 1800.0, "Охранник")

    building_2.add_staff(janitor.name)
    dormitory_4.hire_staff(security.name)

    print("Сотрудники:")
    print(f"  - {janitor.name} ({janitor.role}, зарплата: {janitor.salary} BYN)")
    print(f"  - {security.name} ({security.role}, зарплата: {security.salary} BYN)")

    if janitor.increase_salary_if_short_staffed(building_2, threshold=3):
        print(f"Зарплата {janitor.name} повышена до {janitor.salary} BYN (недокомплект персонала)")
    print(f"Годовая зарплата {janitor.name}: {janitor.get_annual_salary()} BYN")

    print("\n[14] Статистика университета")
    print("Всего корпусов: 3")
    print("Всего общежитий: 2")
    print("Факультетов: 3")
    print("Кафедр: 3")
    print(f"Преподавателей: {len(dept_informatics.teachers) + len(dept_poit.teachers) + len(dept_math.teachers)}")
    print(f"Студентов в группах: {len(group_453503.students) + len(group_451501.students) + len(group_450505.students)}")
    print(f"Выдано стипендий: {rectorate.scholarships_awarded}")
    print(f"Выдано премий: {rectorate.bonuses_awarded}")

    print("\nСценарий завершен успешно!")


if __name__ == "__main__":
    main()