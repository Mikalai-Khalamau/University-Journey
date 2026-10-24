from LR2.Rectorate import Rectorate
from LR2.AcademyBuilding import AcademyBuilding
from LR2.Faculty import Faculty
from LR2.Speciality import Speciality
from LR2.Group import Group
from LR2.Department import Department
from LR2.Discipline import Discipline
from LR2.Student import Student
from LR2.Teacher import Teacher
from LR2.Staff import Staff
from LR2.AcademicRank import AcademicRank
from LR2.ResidencePlace import ResidencePlace
from LR2.Dormitory import Dormitory
from LR2.University import University

def main():
    print("Демонстрационный сценарий")

    print("\n[1] Создание учебных корпусов и общежитий")
    building_2 = AcademyBuilding("Корпус 2", "ул. Петруся Бровки, 4", 2)
    building_1 = AcademyBuilding("Корпус 1", "ул. Петруся Бровки, 6", 1)
    building_3 = AcademyBuilding("Корпус 3", "ул. Петруся Бровки, 8", 3)
    dormitory_4 = Dormitory("Общежитие 4", "пр. Дзержинского, 95", 4, 300)
    dormitory_5 = Dormitory("Общежитие 5", "ул. Семашко, 10", 5, 250)

    print(f"Созданы корпуса: {building_2}, {building_1}, {building_3}")
    print(f"Созданы общежития: {dormitory_4}, {dormitory_5}")

    print("\n[2] Создание администрации")
    rectorate = Rectorate("Богуш")
    rectorate.appoint_vice_rector("Шнейдеров")
    rectorate.appoint_vice_rector("Кузнецов")
    university = University("Белорусский государственный университет информатики и радиоэлектроники", rectorate)
    university.add_building(building_2)
    university.add_building(building_1)
    university.add_building(building_3)
    university.add_dormitory(dormitory_4)
    university.add_dormitory(dormitory_5)

    print(f"{university}")
    print(f"Ректорат: {rectorate.rector} (проректоры: {len(rectorate.vice_rectors)})")

    print("\n[3] Создание факультетов и кафедр")
    fksis = Faculty("ФКСиС", "Ульянов")
    fkp = Faculty("ФКП", "Козлов")
    fitu = Faculty("ФИТУ", "Новиков")

    university.add_faculty(fksis)
    university.add_faculty(fkp)
    university.add_faculty(fitu)

    dept_informatics = Department("Кафедра информатики", "Сиротко")
    dept_poit = Department("Кафедра ПОИТ", "Соколов")
    dept_math = Department("Кафедра высшей математики", "Орлов")

    fksis.open_department_in_building(dept_informatics, building_2)
    fkp.open_department_in_building(dept_poit, building_1)
    fitu.open_department_in_building(dept_math, building_3)

    print(f"Факультеты: {fksis}, {fkp}, {fitu}")
    print(f"Кафедры: {dept_informatics}, {dept_poit}, {dept_math}")

    print("\n[4] Создание преподавателей")
    teacher_siroko = Teacher("Сиротко", "Паспорт: 123456", "+375291112233", AcademicRank.PROFESSOR)
    teacher_sokolov = Teacher("Соколов", "Паспорт: 234567", "+375292223344", AcademicRank.DOCENT)
    teacher_orlov = Teacher("Орлов", "Паспорт: 345678", "+375293334455", AcademicRank.PROFESSOR)

    dept_informatics.add_teacher(teacher_siroko)
    dept_poit.add_teacher(teacher_sokolov)
    dept_math.add_teacher(teacher_orlov)

    print("Преподаватели созданы и назначены на кафедры")

    print("\n[5] Создание дисциплин")
    programming = Discipline("Программирование", 180)
    databases = Discipline("Базы данных", 144)
    math_analysis = Discipline("Математический анализ", 216)

    teacher_siroko.add_discipline(programming)
    teacher_sokolov.add_discipline(databases)
    teacher_orlov.add_discipline(math_analysis)

    print(f"Дисциплины: {programming}, {databases}, {math_analysis}")
    print(f"{programming.name}: преподаватели {', '.join(t.name for t in programming.teachers)}")
    print(f"{databases.name}: преподаватели {', '.join(t.name for t in databases.teachers)}")

    print("\n[6] Создание специальностей и групп")
    spec_iitp = Speciality("IITP", 4, fksis.name)
    spec_poit = Speciality("POIT", 4, fkp.name)
    spec_vm = Speciality("VMA", 4, fitu.name)

    fksis.add_speciality(spec_iitp)
    fkp.add_speciality(spec_poit)
    fitu.add_speciality(spec_vm)

    group_453503 = Group(453503, spec_iitp.name)
    group_451501 = Group(451501, spec_poit.name)
    group_450505 = Group(450505, spec_vm.name)

    spec_iitp.add_group(group_453503)
    spec_poit.add_group(group_451501)
    spec_vm.add_group(group_450505)

    spec_iitp.add_disciplines_to_group(group_453503, [programming, databases, math_analysis])
    spec_poit.add_disciplines_to_group(group_451501, [programming, databases])
    spec_vm.add_disciplines_to_group(group_450505, [math_analysis])

    print(f"Специальности: {spec_iitp}, {spec_poit}, {spec_vm}")
    print(f"Группы: {group_453503}, {group_451501}, {group_450505}")
    print(f"Дисциплины группы {group_453503.number}: {', '.join(d.name for d in group_453503.disciplines)}")
    print(f"Дисциплины группы {group_451501.number}: {', '.join(d.name for d in group_451501.disciplines)}")
    print(f"Дисциплины группы {group_450505.number}: {', '.join(d.name for d in group_450505.disciplines)}")

    print("\n[7] Создание студентов")
    student_ivanov = Student("Иванов", "Паспорт: 456789", "+375294445566", ResidencePlace.MINSK, 1, "Дневная", 0.0)
    student_petrov = Student("Петров", "Паспорт: 567890", "+375295556677", ResidencePlace.NONRESIDENT, 1, "Дневная", 0.0)
    student_sidorov = Student("Сидоров", "Паспорт: 678901", "+375296667788", ResidencePlace.FOREIGNER, 1, "Дневная", 0.0)
    student_kuznetsov = Student("Кузнецов", "Паспорт: 789012", "+375297778899", ResidencePlace.MINSK, 1, "Дневная", 0.0)

    group_453503.add_student(student_ivanov)
    group_453503.add_student(student_petrov)
    group_451501.add_student(student_sidorov)
    group_450505.add_student(student_kuznetsov)

    print("Студенты добавлены в группы")
    print(f"{student_ivanov.name} (группа {student_ivanov.group.number}, курс {student_ivanov.course})")
    print(f"{student_kuznetsov.name} (группа {student_kuznetsov.group.number}, курс {student_kuznetsov.course})")

    print("\n[8] Учебный процесс: преподаватели ставят оценки студентам")
    teacher_siroko.grade_student(student_ivanov, programming, 9)
    teacher_siroko.grade_student(student_ivanov, programming, 10)
    teacher_sokolov.grade_student(student_sidorov, databases, 9)
    teacher_orlov.grade_student(student_kuznetsov, math_analysis, 10)

    print(f"Оценки студента {student_ivanov.name}: GPA = {student_ivanov.gpa}")
    print(f"Оценки студента {student_kuznetsov.name}: GPA = {student_kuznetsov.gpa}")

    print("\n[9] Полиморфизм подтипов: единый интерфейс для разных ролей")
    people = [student_ivanov, teacher_siroko, Staff("Ковалев", "Паспорт: 890123", "+375298889900", 1500.0, "Уборщик")]

    for person in people:
        print(f"[{person.get_role_description()}]")
        print(f"{person.get_contact_info()}")
        print()

    print("\n[10] Ad hoc полиморфизм: метод award() с перегрузкой для разных типов")
    print(rectorate.award(student_ivanov))

    for i in range(7):
        teacher_siroko.add_discipline(Discipline(f"Доп_дисциплина_{i + 1}", 36))
    print(rectorate.award(teacher_siroko))

    janitor = Staff("Ковалев", "Паспорт: 890123", "+375298889900", 1500.0, "Уборщик")
    building_2.add_staff(janitor)
    print(rectorate.award(janitor))

    print(f"Статистика наград: стипендий = {rectorate.scholarships_awarded}, премий = {rectorate.bonuses_awarded}")

    print("\n[11] Параметрический полиморфизм: поиск сущностей по типу")
    all_students = university.find_entities_by_type(Student)
    print(f"Найдено студентов: {len(all_students)}")

    all_teachers = university.find_entities_by_type(Teacher)
    print(f"Найдено преподавателей: {len(all_teachers)}")

    top_students = university.filter_entities(Student, lambda s: s.gpa > 8.0)
    print(f"Отличники (GPA > 8.0): {len(top_students)}")
    for student in top_students:
        print(f"{student.name} (GPA: {student.gpa})")

    all_buildings = university.find_entities_by_type(AcademyBuilding)
    print(f"Найдено учебных корпусов: {len(all_buildings)}")

    print("\n[12] Факультет предоставляет общежитие (условие: GPA > 9.0)")
    if fksis.provide_dormitory(student_ivanov, dormitory_4):
        print(f"Студент {student_ivanov.name} заселён в {dormitory_4.name}")
    else:
        print(f"Студент {student_ivanov.name} не прошёл по баллам (требуется GPA > 9.0)")

    if not fkp.provide_dormitory(student_sidorov, dormitory_5):
        print(f"Студент {student_sidorov.name} не прошёл по баллам (GPA: {student_sidorov.gpa})")

    print("\n[13] Сотрудник увеличивает зарплату при недокомплекте персонала")
    print(f"Текущая зарплата {janitor.name}: {janitor.salary} BYN")
    print(f"Персонал в корпусе '{building_2.name}': {len(building_2.staff)} человек")

    if janitor.increase_salary_if_short_staffed(building_2, threshold=3):
        print(f"Зарплата {janitor.name} повышена до {janitor.salary} BYN (недокомплект персонала)")
    else:
        print(f"Зарплата не повышена (достаточно персонала)")

    print(f"Годовая зарплата: {janitor.get_annual_salary()} BYN")

    print("\n[14] Статистика университета")
    print(university.generate_university_report())

    print("\n[15] Отчёт ректората")
    print(rectorate.generate_report())

    print("\nВиды полиморфизма:")
    print("1. Полиморфизм подтипов: единый интерфейс Person.get_role_description() для Student, Teacher, Staff")
    print("2. Ad hoc полиморфизм: перегрузка Rectorate.award() для разных типов")

    all_students = [student_ivanov, student_petrov, student_sidorov, student_kuznetsov]
    teacher_sokolov.grade_student(student_sidorov, databases, 9)
    otlichniki = university.find_in_collection(all_students, lambda s: s.gpa > 4.0)
    for s in otlichniki:
        print(f"{s.name} (GPA: {s.gpa})")

    academy = AcademyBuilding("Корпус 2", "ул", 2)
    dormitory = Dormitory("Общежитие 4", "пр", 4, 300)


    print(university.print_building_info(academy))

    print(university.print_building_info(dormitory))

if __name__ == "__main__":
    main()