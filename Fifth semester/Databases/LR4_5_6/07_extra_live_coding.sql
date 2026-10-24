-- 1. Вывести фамилию, имя и номер группы всех студентов, чья фамилия заканчивается на «ов» или «ин». Отсортировать результат сначала по номеру группы, а внутри группы — по фамилии

select s.last_name, s.first_name , g.name from students s
join groups g on g.id=s.group_id 
where s.last_name like '%ов' or s.last_name like '%ин'
order by s.group_id ,s.last_name;

-- 2. Показать полное расписание для группы 123456 на конкретную дату ('2026-09-22'). Вывести нужно: время начала, время конца, номер аудитории и название корпуса

select s.start_time, s.end_time, a.number, b.name  from schedule s
join groups g on g.id =s.group_id 
join audiences a on a.id =s.audience_id 
join buildings b on b.id =a.building_id 
where s.lesson_date ='2026-09-22' and g.name='123456';

-- 3. Найти все предметы, по которым еще не создано ни одной учебной нагрузки 

select s.name from subjects s
left join study_load sl on sl.subject_id =s.id 
where sl.id is null;

-- 4. Вывести список всего оборудования, которое находится в корпусах, чье название содержит слово «корпус».

select e.name from equipment e 
join audiences a  on e.audience_id = a.id 
join buildings b on b.id =a.building_id 
where b.name ilike '%Корпус%';

-- 5. Найти всех студентов, которые когда-либо получали оценку 10. Вывести только их ФИО.

select distinct s.first_name, s.last_name from rating r
join students s on s.id =r.student_id 
where r.val = 10;

-- Способ красивый спасибо квен

select first_name, last_name from students
where id in (select student_id from rating where val=10);


-- 6. Вывести список преподавателей, которые не ведут ни одного занятия

select p.first_name, p.last_name from prepods p
left join lessons l on l.prepod_id =p.id 
where l.prepod_id is null;

-- 7. Показать все оценки, выставленные в октябре 2026 года, где сама оценка больше 7. Вывести нужно дату, значение оценки, ФИО студента и название предмета.

select r.val, r.rating_date, s."name" ,st.first_name ,st.last_name from rating r
join study_load sl on sl.id =r.study_id 
join subjects s on s.id =sl.subject_id 
join students st on st.id =r.student_id 
where r.rating_date between '2026-10-01' and '2026-10-31' and r.val>7;

-- 8. Найти всех студентов, которые учатся в той же группе, что и студент с фамилией 'Иванов'. Самого Иванова в список не включать.

select students.last_name from students 
where students.group_id in (select students.group_id from students where students.last_name='Иванов') and students.last_name !='Иванов';

-- 9. Вывести информацию о всех мероприятиях, указав дату, название мероприятия, ФИО ответственного преподавателя и название его факультета.

select e.event_date ,e.name ,p.last_name ,p.first_name ,f."name"  from events e
join prepods p on p.id =e.prepod_id 
join faculty f on f.id =p.faculty_id ;

-- 10. Найти все аудитории на 2-м этаже, в которых нет ни одного предмета оборудования.

select a.number from audiences a 
left join equipment e on e.audience_id =a.id 
where a.floor ='2' and e.id is null;


--1. Подсчитать количество студентов в каждой группе. Вывести название группы (groups.name) и количество студентов.

select g.id, count(s.id) from students s
left join groups g on s.group_id =g.id
group by g.id;

-- 2. Для каждого преподавателя вывести его ФИО и общее количество поставленных им оценок. Отсортировать список от тех, кто поставил больше всех, к тем, кто меньше.

select p.first_name ,p.last_name , count(r.val) from prepods p
left join rating r on r.prepod_id =p.id 
group by p.first_name ,p.last_name 
order by count(r.val) desc;

--3. Найти предметы, средняя оценка по которым строго больше 8. Вывести название предмета и его среднюю оценку.

select s.name,avg(r.val) from subjects s
left join study_load sl on s.id=sl.subject_id 
left join rating r on r.study_id =sl.id 
group by s.id ,s.name
having avg(r.val)>8;

-- Студенты с оценкой больше 8

WITH student_avg AS (
    SELECT student_id, AVG(val) AS avg_rating
    FROM rating
    GROUP BY student_id
)
SELECT s.last_name, s.first_name, sa.avg_rating
FROM students s
JOIN student_avg sa ON s.id = sa.student_id
WHERE sa.avg_rating > 8
ORDER BY sa.avg_rating DESC;


--4. Вывести список групп и максимальную оценку, полученную хотя бы одним студентом в этой группе.

select g.name, max(r.val) from groups g
join students s on s.group_id =g.id 
join rating r on r.student_id =s.id
group by g.id , g.name;

--5. Вывести список преподавателей и количество поставленных ими оценок.

select p.last_name, count(r.val) from prepods p
left join rating r on r.prepod_id =p.id
group by p.id, p.last_name;

-- 11. Вывести преподов с расписанием и аудиториями

SELECT  p.last_name || ' ' || p.first_name AS prepod_fio, s.lesson_date, s.start_time, s.end_time, a.number AS audience_number
FROM prepods p
JOIN lessons l ON l.prepod_id = p.id
JOIN schedule s ON s.group_id = l.group_id  
JOIN audiences a ON a.id = s.audience_id
ORDER BY p.last_name, s.lesson_date, s.start_time;


-- 12. Создать представление student_progress, которое показывает для каждого студента его ФИО, группу, количество полученных оценок и средний балл. 
-- Затем использовать это представление, чтобы найти студентов со средним баллом выше 8.

CREATE VIEW student_progress AS
SELECT 
    s.id AS student_id,
    s.last_name || ' ' || s.first_name AS student_fio,
    g.name AS group_name,
    COUNT(r.id) AS ratings_count,
    ROUND(AVG(r.val), 2) AS avg_rating
FROM students s
LEFT JOIN groups g ON g.id = s.group_id
LEFT JOIN rating r ON r.student_id = s.id
GROUP BY s.id, s.last_name, s.first_name, g.name;

-- Показать всех студентов с их прогрессом
SELECT * FROM student_progress
ORDER BY avg_rating DESC NULLS LAST;

-- Найти студентов со средним баллом выше 8
SELECT student_fio, group_name, avg_rating
FROM student_progress
WHERE avg_rating > 8;

-- Найти студентов без оценок
SELECT student_fio, group_name
FROM student_progress
WHERE ratings_count = 0 OR ratings_count IS NULL;


-- Пример агрегирующей функции

SELECT group_id, AVG(val) AS avg_rating
FROM rating r
union students s on s.id = r.id 
join "groups" g on g.id = s.group_id 
GROUP BY group_id;

union



-- Пример оконной функции

select student_id, group_id, val, AVG(val) OVER (PARTITION BY group_id) AS group_avg
FROM rating r 
join students s on s.id = r.id 
join "groups" g on g.id = s.group_id ;

-- Логирование изменений оценок

-- Каждый раз, когда преподаватель меняет оценку студенту, записывать в отдельную таблицу rating_log старое значение, новое значение, дату изменения и кто изменил.

CREATE TABLE rating_log (
    id SERIAL PRIMARY KEY,
    rating_id INT,
    student_id INT,
    old_val INT,
    new_val INT,
    changed_at TIMESTAMP DEFAULT NOW(),
    operation VARCHAR(10)
);

CREATE OR REPLACE FUNCTION log_rating_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, что оценка реально изменилась
    IF OLD.val IS DISTINCT FROM NEW.val THEN
        INSERT INTO rating_log (rating_id, student_id, old_val, new_val, operation)
        VALUES (OLD.id, OLD.student_id, OLD.val, NEW.val, TG_OP);
    END IF;
    
    RETURN NEW;  -- возвращаем новую строку, чтобы UPDATE продолжился
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_rating_update
    AFTER UPDATE
    ON rating
    FOR EACH ROW
    EXECUTE FUNCTION log_rating_changes();

-- Допустим, у студента была оценка 7
SELECT * FROM rating WHERE id = 1;

-- Преподаватель исправляет оценку на 9
UPDATE rating SET val = 9 WHERE id = 1;

-- Триггер записал в лог:
SELECT * FROM rating_log;



-- 6. Для каждого факультета посчитать общее количество студентов и средний балл всех студентов этого факультета.

select f.name, count(distinct s.id), avg(r.val) from faculty f
left join groups g on g.faculty_id =f.id
left join students s on s.group_id=g.id 
left join rating r on r.student_id =s.id 
group by f.id, f.name;

-- 7. Вывести месяц (число от 1 до 12), в который было выставлено больше всего оценок.

select EXTRACT(MONTH FROM r.rating_date) from rating r
group by EXTRACT(MONTH FROM r.rating_date)
order by count(r.val) desc
limit 1;

--8. Найти студентов, у которых в таблице rating более 2 записей об оценках. Вывести их ФИО и количество оценок.

select s.last_name, count(r.val) from students s
join rating r on r.student_id =s.id 
group by s.id, s.last_name 
having count(r.val)>2;

--9. Вывести ФИО студентов и их средний балл, но только для тех студентов, чей средний балл выше общего среднего балла по всему университету.

select s.last_name, avg(r.val) from students s
left join rating r on r.student_id =s.id
group by s.id, s.last_name
having avg(r.val)> (select avg(rating.val) from rating);


--10. Для каждого преподавателя посчитать количество уникальных предметов, по которым он ставил оценки.

select p.last_name, count(distinct s.id) from prepods p
left join rating r on r.prepod_id =p.id
left join study_load sl on sl.id=r.study_id 
left join subjects s on s.id=sl.subject_id
group by p.id, p.last_name ;



-- Вывести все здания + аудитории которые заняты 22.09.2026

select * from schedule;

select distinct b.name, a.number from buildings b 
join audiences a on a.building_id = b.id 
join schedule s on s.audience_id =a.id 
where s.lesson_date != '29-09-2026'
group by b.name, a.id , a.number;



