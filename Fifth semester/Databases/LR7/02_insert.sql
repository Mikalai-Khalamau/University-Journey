insert into lines (name, color, number) values
('Московская', 'синий', 1),
('Автозаводская', 'красный', 2),
('Зеленолужская', 'зеленый', 3);

insert into passengers (full_name, phone, email) values
('Хадорик Матвей Денисович', '+275291234567', 'khadoryk@gmail.com'),
('Бокун Артем Геннадьевич', '3752912334567', 'bokun@gmail.com'),
('Гламаздин Игорь Иванович', '375291234567', 'i.glamazdin@gmail.com');

insert into system_users (login, password_hash, role) values
('admin', 'hashed_password_admin', 'admin'),
('dispatcher1', 'hashed_password_disp1', 'user'),
('cashier1', 'hashed_password_cash1', 'user');

insert into stations (line_id, name, depth, has_escalator) values
(1, 'Петровщина', 83, false),
(1, 'Площадь Ленина', 110, true),
(1, 'Борисовский тракт', 312, false),
(2, 'Кунцевщина', 36, false),
(2, 'Могилевская', 15, false),
(3, 'Слуцкий гостинец', 40, true),
(3, 'Юбилейная пощадь', 3675, true);

insert into trains (line_id, number, model, status) values
(1, '8001', 'Минск 2024', 'line'),
(1, '8002', 'Москва-2020', 'depo'),
(2, '7001', 'Беларус', 'line'),
(3, '5001', 'Олег', 'renovation');

insert into equipment (station_id, type, name, status) values
(1, 'турникет', 'турникет 1', 'ok'),
(1, 'эскалатор', 'эскалатор 1', 'ok'),
(2, 'турникет', 'турникет 2', 'broke'),
(3, 'вентилятор', 'вентилятор 1', 'ok'),
(6, 'эскалатор', 'эскалатор 3', 'renovation');

insert into trips (train_id, station_id, departure_time, arrival_time, trip_date, status) values
(1, 1, '08:00:00', '08:15:00', '2024-01-15', 'on schedule'),
(1, 2, '08:20:00', '08:35:00', '2024-01-15', 'delayed'),
(3, 4, '09:00:00', '09:30:00', '2024-01-15', 'on schedule'),
(3, 5, '09:35:00', '10:05:00', '2024-01-15', 'cancelled');

insert into passes (passenger_id, type, balance, expiration_date) values
(1, 'month', 30, '2024-02-15'),
(2, 'day', 1, '2024-01-20'),
(3, 'decade', 10, '2024-01-25');

insert into incidents (equipment_id, reported_id, description, status) values
(3, 2, 'турникет не принимает карты', 'work'),
(5, 3, 'эскалатор издаёт посторонние звуки', 'open');

insert into action_logs (user_id, action_type, entity_name, entity_id) values
(1, 'insert', 'system_users', 2),
(1, 'insert', 'system_users', 3),
(2, 'insert', 'incidents', 1),
(3, 'insert', 'incidents', 2);