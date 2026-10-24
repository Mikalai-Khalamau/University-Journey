drop table if exists action_logs cascade;
drop table if exists incidents cascade;
drop table if exists passes cascade;
drop table if exists trips cascade;
drop table if exists equipment cascade;
drop table if exists trains cascade;
drop table if exists stations cascade;
drop table if exists lines cascade;
drop table if exists passengers cascade;
drop table if exists system_users cascade;

-- 1. Ветки метро
create table lines(
id serial primary key,
name varchar(50) not null,
color varchar(20) not null,
number int not null unique);

-- 2. Пассажиры
create table passengers(
id serial primary key,
full_name varchar(200) not null,
phone varchar(20),
email varchar(100)
);

-- 3. Пользователи системы
create table system_users (
id serial primary key,
login varchar(50) not null unique,
password_hash varchar(255) not null,
role varchar(20) not null check (role in ('user','admin')),
created_at timestamp default current_timestamp);

-- 4. Станции метро, привязаны к веткам

create table stations(
id serial primary key,
line_id int not null,
name varchar(100) not null,
depth int,
has_escalator boolean default false,
foreign key (line_id) references lines(id) on delete cascade);

-- 5. Поезда, привязаны к веткам

create table trains(
id serial primary key,
line_id int not null,
number varchar(20) not null unique,
model varchar(50) not null,
status varchar(20) not null default 'depo' check (status in ('line', 'depo','renovation')),
foreign key (line_id) references lines(id) on delete cascade
);

-- 6. Оборудование на станциях

create table equipment(
id serial primary key,
station_id int not null,
type varchar(50) not null,
name varchar(100) not null,
status varchar(20) not null default 'ok' check (status in ('ok','broke','renovation')),
foreign key (station_id) references stations(id) on delete cascade);

-- 7. Рейсы поезда от станции до станции по расписанию. Станция - начало рейса

create table trips (
id serial primary key,
train_id int not null,
station_id int not null,
departure_time time not null,
arrival_time time not null,
trip_date date not null,
status varchar(20) not null default 'on schedule' check (status in ('on schedule', 'delayed', 'cancelled')),
foreign key (train_id) references trains(id) on delete cascade,
foreign key (station_id) references stations(id) on delete cascade);


-- 8. Проездные для пассажиров

create table passes (
id serial primary key,
passenger_id int not null,
type varchar(50) not null check (type in ('day','month','decade')),
balance int not null default 0,
expiration_date date not null,
foreign key (passenger_id) references passengers(id) on delete cascade);

-- 9. Инциденты и поломки оборудования, сообщаемые пользователями

create table incidents (
id serial primary key,
equipment_id int not null,
reported_id int not null,
description text,
status varchar(20) not null default 'open' check (status in ('open', 'work', 'fixed')),
created_at timestamp default current_timestamp,
foreign key (equipment_id) references equipment(id) on delete cascade,
foreign key (reported_id) references system_users(id) on delete cascade);

-- 10. Журнал действий с пользователями системы

create table action_logs (
id serial primary key,
user_id int not null,
action_type varchar(50) not null check (action_type in ('insert', 'update', 'delete', 'login')),
entity_name varchar(50) not null,
entity_id int,
timestamp timestamp default current_timestamp,
foreign key (user_id) references system_users(id) on delete cascade);

