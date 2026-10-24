--1. Определить количество прошедших занятий

select count(*) from lessons;

--2. Вывести 10 лучших студентов по средней оценке
select s.last_name, avg(r.val) as average_rating from students s
join rating r on r.student_id=s.id 
group by s.id, s.last_name
order by average_rating desc
limit 10;

-- 3. Получить количество предметов и типов занятий по которым стоят оценки

select count(distinct s.subject_id) ,count(distinct s.type_study_id) from rating r
join study_load s on s.id =r.study_id ;

-- 4. Вывести список преподавателей отсортированный по количеству оценок, которые они поставили

select p.last_name || ' ' || p.first_name, count(val) from rating r
join prepods p on p.id =r.prepod_id 
group by p.id, p.first_name , p.last_name 
order by count(val) asc;

-- 5. Вывести фамилии студентов у которых нет ни одной оценки

insert into students (id, last_name, first_name, group_id) values (11111, 'Муха', 'Артемий', 1);

select s.last_name from students s
left join rating r on s.id=r.student_id 
group by s.id, s.last_name 
having count(r.val)=0;
-- можно where r.id is null

--6.  Вывести информацию о студенте средняя оценка которого максимальна

select s.id, s.last_name, s.first_name, s.group_id, avg(r.val) from rating r
join students s on s.id =r.student_id 
group by s.id, s.last_name, s.first_name, s.group_id
order by avg(r.val) desc
limit 1;


