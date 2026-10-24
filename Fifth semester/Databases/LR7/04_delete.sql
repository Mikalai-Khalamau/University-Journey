delete from trips
where status = 'cancelled' and id = 4;

update incidents
set status = 'fixed'
where id = 1;

delete from incidents
where status = 'fixed' and id = 1;

insert into action_logs (user_id, action_type, entity_name, entity_id) values
(2, 'delete', 'trips', 4),
(3, 'delete', 'incidents', 1);