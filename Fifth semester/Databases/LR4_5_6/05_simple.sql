-- 1. Построить запрос, формирующий вывод всех данных обо всех преподавателях

select * from prepods;

-- 2. Построить запрос, формирующий вывод фамилии и имени студентов, обучающихся в первой группе отсортированные в алфавитном порядке по фамилии

insert into groups (id, name) values (1, '1');
insert into students (id, last_name, first_name, group_id) values (11, 'Иваунов', 'Никита', 1), (12, 'Петуров', 'Митрофан', 1);

select last_name, first_name from students where group_id=1 order by last_name asc;

--3. Вывести данные о студентах, фамилии которых начинаются на букву О

insert into students (id, last_name, first_name, group_id) values (13, 'Олегов', 'Никита', 1), (14, 'Олежкин', 'Митрофан', 1);

select * from students where last_name like 'О%';

-- 4. Вывести все оценки, которые поставил преподаватель Проволоцкий В.Е. в октябре 2020 года

insert into prepods (id, last_name, first_name, faculty_id) values (22, 'Проволоцкий', 'Владимир', 1);

insert into rating (id, rating_date, val, student_id, study_id, prepod_id) values (100, '2020-10-05', 8, 1, '67', 22), (101, '2020-10-12', 9, 2, '67', 22), (104, '2020-10-19', 7, 3, '67', 22);

-- Хардкод айдишника Проволоцкого
-- select val from rating where prepod_id=22 and rating_date between '2020-10-01' and '2020-10-31';

select r.val, r.student_id, r.rating_date from rating r
join prepods p on r.prepod_id=p.id
where p.last_name='Проволоцкий' and p.first_name='Владимир'
and r.rating_date between '2020-10-01' and '2020-10-31';


-- 5.Вывести всех студентах которые отсутствовали на лекциях.

select distinct s.last_name from rating r
join students s on r.student_id=s.id 
where r.is_absent='Y';

-- 6. Вывести информацию о полученной оценке с указанием наименования факультета, группы фио студента и преподавателя оценки и даты выставления

update groups set faculty_id = 1 where id = 123456;

select r.val, f.name as faculty, g.name as group_name, s.first_name || ' ' || s.last_name , p.first_name || ' ' || p.last_name , r.rating_date from rating r
join students s on s.id=r.student_id 
join prepods p on p.id=r.prepod_id 
join groups g on g.id=s.group_id
join faculty f on f.id=g.faculty_id;

-- 7. Вывести информацию о занятиях во время которых оценки выставлялись не основными(включенными в план) преподавателями

select r.rating_date, r.val, s.first_name || ' ' || s.last_name as student, plan_prepod.first_name || ' ' || plan_prepod.last_name as plan_prepod, real_prepod.first_name || ' ' || real_prepod.last_name as real_prepod from rating r
join students s on s.id=r.student_id 
join lessons l on l.group_id=s.group_id and l.study_id=r.study_id 
join prepods real_prepod on real_prepod.id=r.prepod_id 
join prepods plan_prepod on plan_prepod.id=l.prepod_id 
where r.prepod_id != l.prepod_id ;

-- 8. Вывести отсортированный по фамилиям (прямом в порядке) список преподавателей и номера групп, в которых они ставили оценки.

insert into groups (id, name) values (2, '2');
insert into rating (id, rating_date, val, student_id, study_id, prepod_id) values (1010, '2020-10-05', 8, 11, '67', 22);
insert into rating (id, rating_date, val, student_id, study_id, prepod_id) values (1011, '2020-10-05', 8, 11, '67', 1);

select distinct p.last_name || ' ' || p.first_name as prepod_name, g.name from prepods p
join rating r on r.prepod_id =p.id 
join students s on s.id=r.student_id 
join groups g on g.id =s.group_id 
order by prepod_name asc;

-- 9.  Вывести отсортированный по фамилиям (прямом в порядке) список всех преподавателей и номера групп, в которых они ставили оценки.

select distinct p.last_name || ' ' || p.first_name as prepod_name, g.name from prepods p
left join rating r on r.prepod_id =p.id 
left join students s on s.id=r.student_id 
left join groups g on g.id =s.group_id 
order by prepod_name asc;

-- 10. Вывести коды и названия факультетов в которых нет групп

select f.id, f.name from faculty f
left join groups g on g.faculty_id =f.id 
where g.id is null;


