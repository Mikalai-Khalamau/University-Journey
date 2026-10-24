-- 1. Добавить новую группу с номером 123456
-- Пока не добавляем факультет и старосту, но сделаем это позже

insert into groups (id, name) values (123456, '123456');

select * from groups where id = 123456;

--2. Внести в групп 123456 студентов Иванова и Петрова

insert into students (id, last_name, first_name, group_id) values (1, 'Иванов', 'Никита', 123456), (2, 'Петров', 'Митрофан', 123456) returning *;

-- Или можем с обычной проверочкой

-- select * from students where group_id=123456;

--3. Назначить студента Иванова старостой группы

-- update groups 
-- set head_group=1
-- where id=123456
-- returning *;

-- Вариант посложнее, чтобы жёстко не привязываться к господину Никите Иванову и его айдишнику

update groups
set head_group=(select id from students where last_name='Иванов' and first_name='Никита')
where id=123456;

select * from groups where id=123456;

--4. Добавить факультеты КСИС и ФИТУ

insert into faculty (id, name) values (1, 'ФКСиС'), (2, 'ФИТиУ') returning *;

--5. Добавить преподавателей Васечкина и Петечкина на факультеты КСИС и ФИТУ соответственно

insert into prepods (id, last_name, first_name, faculty_id) values (1, 'Васечкин', 'Антон', 1), (2, 'Петечкин', 'Матвей', 2) returning *;


--6. Назначить преподавателю Васечкину ведение предмета «Введение в специальность» для группы 123456

-- insert into subjects (id, name) values (101, 'Введение в специальность');

-- insert into study_load (id, subject_id) values (67, 101);

-- insert into lessons (group_id, prepod_id, study_id) values (123456, 1, 67) returning *;

-- Вариант полный для нёрдов

insert into subjects (id, name, faculty_id) values (101, 'Введение в специальность', 1);

insert into type_study_load (id, name) values (1, 'Семинары');

insert into study_load (id, hours, subject_id, type_study_id) values (67, 20, 101, 1);

insert into lessons (group_id, prepod_id, study_id) values (123456, 1, 67) returning *;


--7. Поставить Студенту Иванову по предмету «Введение в специальность» оценку 10, отметить отсутствие студента Петрова на данном занятии

insert into rating (id, rating_date, val, student_id, study_id) values (1, '2026-09-22', 10, 1, 67) returning *;

insert into rating (id, rating_date, student_id, study_id, is_absent) values (2, '2026-09-22', 2, 67, 'Y') returning *;

-- 8. Наполнить базу таким образом, чтобы в базе появилась информация по различным
-- предметам (минимум 4), по каждому из которых стояло бы не менее 3 отметок(минимум 5 студентам )

insert into subjects (id, name, faculty_id) values (200, 'Основы алгоритмизации', 1);
insert into subjects (id, name, faculty_id) values (201, 'Математический анализ', 1);
insert into subjects (id, name, faculty_id) values (202, 'Современные платформы прикладной разработки', 1);
insert into subjects (id, name, faculty_id) values (203, 'Основы информационной безопасности', 2);
insert into subjects (id, name, faculty_id) values (204, 'Маркетинг', 2);

insert into type_study_load (id, name) values (2, 'Лекции');
insert into type_study_load (id, name) values (3, 'Лабораторные');

insert into study_load (id, hours, subject_id, type_study_id) values (type(80, decimal), 108, 200, 3);
insert into study_load (id, hours, subject_id, type_study_id) values (type(80, decimal), 13268, 222200, 3);
insert into study_load (id, hours, subject_id, type_study_id) values (81, 108, 201, 2);
insert into study_load (id, hours, subject_id, type_study_id) values (82, 108, 202, 3);
insert into study_load (id, hours, subject_id, type_study_id) values (83, 108, 203,1);
insert into study_load (id, hours, subject_id, type_study_id) values (84, 108, 204, 1);

insert into students (id, last_name, first_name, group_id) values (3, 'Хадорик', 'Матвей', 123456), (4, 'Савинов', 'Арсений', 123456), (5, 'Михалко', 'Александр', 123456) returning *;
insert into students (id, last_name, first_name, group_id) values (6, 'Морозова', 'Эвелина', 123456), (7, 'Белобровик', 'Евгений', 123456), (8, 'Данилович', 'Влаидимир', 123456) returning *;

insert into lessons (group_id, prepod_id, study_id) values (123456, 1, 80), (123456, 1, 81), (123456, 1, 82), (123456, 1, 83), (123456, 1, 84) returning *;

insert into rating (id, rating_date, val, student_id, study_id) values (10, '2026-10-14', 10, 2, '80') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (11, '2026-10-14', 6, 3, '80') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (12, '2026-10-14', 7, 4, '80') returning *;

insert into rating (id, rating_date, val, student_id, study_id) values (13, '2026-10-14', 10, 5, '81') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (14, '2026-10-14', 6, 6, '81') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (15, '2026-10-14', 7, 7, '81') returning *;

insert into rating (id, rating_date, val, student_id, study_id) values (16, '2026-10-14', 10, 8, '82') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (17, '2026-10-14', 6, 1, '82') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (18, '2026-10-14', 7, 2, '82') returning *;

insert into rating (id, rating_date, val, student_id, study_id) values (19, '2026-10-14', 10, 3, '83') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (102, '2026-10-14', 6, 4, '83') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (120, '2026-10-14', 7, 5, '83') returning *;

insert into rating (id, rating_date, val, student_id, study_id) values (1220, '2026-10-14', 10, 6, '84') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (1130, '2026-10-14', 6, 7, '84') returning *;
insert into rating (id, rating_date, val, student_id, study_id) values (1110, '2026-10-14', 7, 8, '84') returning *;