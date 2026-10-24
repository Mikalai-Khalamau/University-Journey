update trains
set status = 'line'
where number = '8002';

update passes
set balance = balance - 1
where id = 2;

update incidents
set status = 'work'
where id = 2;

update trips
set departure_time = '08:25:00', arrival_time = '08:40:00', status = 'delayed'
where id = 2;

insert into action_logs (user_id, action_type, entity_name, entity_id) values
(1, 'update', 'trains', 2),
(2, 'update', 'passes', 2),
(3, 'update', 'incidents', 2),
(2, 'update', 'trips', 2);