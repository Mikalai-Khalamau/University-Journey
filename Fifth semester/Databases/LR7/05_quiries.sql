-- много разных запросиков

-- 1 Dывести все станции Московской линии, отсортированные по глубине
select name, depth, has_escalator 
from stations 
where line_id = (select id from lines where name = 'Московская')
order by depth desc;

-- 2 Найти пассажиров, чья фамилия начинается на 'Х' или содержит 'ов'
-- Незадача - у меня фулл имя поэтому ов может быть внутри отчества)
select full_name, phone 
from passengers 
where full_name ilike 'Х%' or full_name ilike '%ов%';

-- 3 Вывести проездные, срок действия которых истекает в ближайшие 30 дней
select passenger_id, type, balance, expiration_date 
from passes 
where expiration_date between current_date and current_date + interval '30 days';

-- 2. объединения таблиц через джоины

-- 4 Полный список оборудования с указанием станции и линии 
select e.name as equipment_name, e.type, e.status, s.name as station_name, l.name as line_name
from equipment e
join stations s on e.station_id = s.id
join lines l on s.line_id = l.id;

-- 5. список всех инцидентов с названием оборудования, станции и логином того, кто сообщил
select i.description, i.status, eq.name as equipment, st.name as station, u.login as reporter
from incidents i
join equipment eq on i.equipment_id = eq.id
join stations st on eq.station_id = st.id
join system_users u on i.reported_id = u.id;

-- 6. расписание рейсов с названием поезда, его моделью и станцией отправления
select t.departure_time, t.arrival_time, t.status, tr.model, tr.number as train_number, st.name as station
from trips t
join trains tr on t.train_id = tr.id
join stations st on t.station_id = st.id;

-- Агрегация и группировка

-- 7. подсчитать количество станций на каждой линии
select l.name as line_name, count(s.id) as stations_count
from lines l
left join stations s on l.id = s.line_id
group by l.id, l.name
order by stations_count desc;

-- 8. найти среднюю глубину станций для каждой линии
select l.name, round(avg(s.depth), 2) as avg_depth
from lines l
join stations s on l.id = s.line_id
group by l.id, l.name;

-- 9. количество инцидентов по каждому типу оборудования
select e.type, count(i.id) as incidents_count
from equipment e
left join incidents i on e.id = i.equipment_id
group by e.type
order by incidents_count desc;

-- 10. найти линии, на которых средняя глубина станций больше 50 метров
select l.name, avg(s.depth) as avg_depth
from lines l
join stations s on l.id = s.line_id
group by l.id, l.name
having avg(s.depth) > 50;

-- Подзапросы и common table expressions

-- 11. найти линии, на которых более 2 станций, и вывести их названия
with line_stats as (
    select line_id, count(id) as cnt
    from stations
    group by line_id
)
select l.name 
from lines l
join line_stats ls on l.id = ls.line_id
where ls.cnt > 2;

-- 12. найти пассажиров, у которых есть проездной типа 'month'
select full_name, phone 
from passengers 
where id in (select passenger_id from passes where type = 'month');

-- 13. найти станцию, которая является самой глубокой во всем метро
select name, depth 
from stations 
where depth = (select max(depth) from stations);

-- 14. найти пользователей, которые не сообщали ни об одном инциденте
select login, role 
from system_users 
where id not in (select distinct reported_id from incidents where reported_id is not null);

-- Оконные функции

-- 15. ранжирование станций по глубине внутри каждой линии 
select l.name as line_name, s.name as station_name, s.depth,
       rank() over (partition by s.line_id order by s.depth desc) as depth_rank
from stations s
join lines l on s.line_id = l.id;

-- 16. нарастающий итог инцидентов, зарегистрированных каждым пользователем
select reported_id, created_at, description,
       sum(1) over (partition by reported_id order by created_at) as total_incidents_by_user
from incidents
order by reported_id, created_at;

-- 17. присвоить порядковый номер каждому рейсу конкретного поезда по времени отправления
select train_id, departure_time, station_id,
       row_number() over (partition by train_id order by departure_time) as trip_number
from trips;

-- Даты и строки

-- 18. вывести месяц (число от 1 до 12), в который было совершено больше всего рейсов
select extract(month from trip_date) as month_num, count(id) as trips_count
from trips
group by extract(month from trip_date)
order by trips_count desc
limit 1;

-- 19. сформировать красивый отчет: "Станция [имя] находится на линии [имя] на глубине [глубина] м"
select 'Станция ' || s.name || ' находится на линии ' || l.name || ' на глубине ' || s.depth || ' м' as report_string
from stations s
join lines l on s.line_id = l.id;

-- 20. найти все рейсы, которые состоялись в понедельник (1 = понедельник в postgresql)
select departure_time, station_id, trip_date
from trips
where extract(isodow from trip_date) = 1;

-- Условия

-- 21. перевести статусы оборудования в понятный текстовый вид
select name, type,
       case status
           when 'ok' then 'Работает исправно'
           when 'broke' then 'Требует срочного ремонта'
           when 'renovation' then 'На плановом обслуживании'
           else 'Неизвестный статус'
       end as status_description
from equipment;

-- 22. категоризация пассажиров по остатку баланса проездного
select p.full_name, ps.balance,
       case 
           when ps.balance = 0 then 'Баланс исчерпан'
           when ps.balance < 5 then 'Низкий баланс'
           else 'Баланс в норме'
       end as balance_status
from passengers p
join passes ps on p.id = ps.passenger_id;

-- Представления

-- 23. топ-3 станции с наибольшим количеством инцидентов
select st.name as station_name, count(i.id) as incidents_count
from stations st
join equipment e on st.id = e.station_id
left join incidents i on e.id = i.equipment_id
group by st.id, st.name
order by incidents_count desc
limit 3;

-- 24. активность пользователей системы: кто и сколько действий совершил
select u.login, u.role, al.action_type, count(al.id) as actions_count
from system_users u
join action_logs al on u.id = al.user_id
group by u.id, u.login, u.role, al.action_type
order by actions_count desc;

-- 25. создание представления для сводного отчета по станциям
create or replace view station_summary as
select 
    s.name as station_name,
    l.name as line_name,
    count(distinct e.id) as equipment_count,
    count(distinct i.id) as incidents_count
from stations s
join lines l on s.line_id = l.id
left join equipment e on s.id = e.station_id
left join incidents i on e.id = i.equipment_id
group by s.id, s.name, l.name;

-- использование представления
select * from station_summary order by incidents_count desc;