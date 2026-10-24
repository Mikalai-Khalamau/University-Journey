-- 1. Удаляем существующие индексы (если они есть)
drop index if exists idx_trips_train_id;
drop index if exists idx_trips_trip_date;

-- 2. Очищаем таблицу trips от тестовых данных (оставляем только исходные 4 рейса)
delete from trips where id > 4;

-- Сбрасываем счётчик автоинкремента
alter sequence trips_id_seq restart with 5;

-- 3. Генерируем 500 новых рейсов для демонстрации
insert into trips (train_id, station_id, departure_time, arrival_time, trip_date, status)
select 
    (random() * 3 + 1)::int as train_id,
    (random() * 6 + 1)::int as station_id,
    (time '08:00:00' + (random() * interval '12 hours'))::time as departure_time,
    (time '08:15:00' + (random() * interval '12 hours'))::time as arrival_time,
    (date '2024-01-15' + (random() * interval '30 days'))::date as trip_date,
    case 
        when random() < 0.8 then 'on schedule'
        when random() < 0.9 then 'delayed'
        else 'cancelled'
    end as status
from generate_series(1, 500);

-- Проверяем количество записей
select count(*) as total_trips from trips;

-- 4. Обновляем статистику PostgreSQL
analyze trips;

-- 5. План выполнения без индексов
explain analyze
select t.id, t.departure_time, t.arrival_time, t.status, st.name as station_name
from trips t
join stations st on t.station_id = st.id
where t.train_id = 1 and t.trip_date = '2024-01-15';

-- 6. СОздали индексы
create index idx_trips_train_id on trips(train_id);
create index idx_trips_trip_date on trips(trip_date);

-- Обновляем статистику после создания индексов
analyze trips;

-- 7. План выполнения с индексами
explain analyze
select t.id, t.departure_time, t.arrival_time, t.status, st.name as station_name
from trips t
join stations st on t.station_id = st.id
where t.train_id = 1 and t.trip_date = '2024-01-15';