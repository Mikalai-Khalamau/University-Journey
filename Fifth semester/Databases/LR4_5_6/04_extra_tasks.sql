-- Дополнительные задания для повышенной оценки, придуманные самим Квеном

-- 1. Добавить в базу 2 новых корпуса. В первом корпусе создать 3 аудитории с разной вместимостью, во втором — 1 аудиторию.

insert into buildings (id, name, address) values (1, '1 корпус ', 'Бровки, 6') returning *;
insert into buildings (id, name, address) values (4, '4 корпус ', 'Гикало, 9') returning *;

insert into audiences (id, number, building_id) values (202, '202', 1);
insert into audiences (id, number, building_id) values (302, '302', 1);
insert into audiences (id, number, building_id) values (666, '666', 1);
insert into audiences (id, number, building_id) values (22, '22', 4);

-- 2. Добавить минимум 4 единицы оборудования и распределить их по разным аудиториям. Одну единицу оборудования переместить из одной аудитории в другую.

insert into equipment (id, name, audience_id) values (1, 'Анисимов Владимир Яковлевич', 202), (2, 'Компьютер Галковского', 302), (3, 'Перфокарта', 666), (4, 'Допустим проектор', 22);

update equipment set audience_id=666 where id=1;

-- 3. Составить расписание для группы 123456 на 3 учебных дня. В каждый день должно быть минимум 2 занятия в разных аудиториях и в разное время. Одно из занятий перенести на другой день.

insert into schedule (id, lesson_date, start_time, end_time, audience_id, group_id) values (1, '2026-09-22', '10:05','11:30', 202, 123456), (2, '2026-09-22', '12:00','13:25', 302, 123456);
insert into schedule (id, lesson_date, start_time, end_time, audience_id, group_id) values (12, '026-09-23', '10:05','11:30', 202, 123456), (21, '026-09-23', '12:00','13:25', 302, 123456);
insert into schedule (id, lesson_date, start_time, end_time, audience_id, group_id) values (221, '026-09-24', '10:05','11:30', 202, 123456), (122, '2026-09-24', '12:00','13:25', 302, 123456);

update schedule set lesson_date='2026-01-11' where lesson_date='2022-12-12' and start_time='10:05';

-- 4. Добавить научное мероприятие, назначить ответственным преподавателя Петечкина. После этого поменять ответственного на Васечкина.

insert into events (id, name, event_date, prepod_id) values (1, 'Научная конференция каф. Информатики', '2011-03-23', 1);
update events set prepod_id=2 where id=1;

--5. Удалить всё оборудование из аудиторий, которые находятся на 2-м этаже любого корпуса. Перед удалением вывести список того, что будет удалено 

delete from equipment where audience_id in (select id from audiences where floor=2) returning *; 