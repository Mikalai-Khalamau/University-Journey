-- 1. создание функции для журналирования 

create or replace function log_action(
    p_user_id int,
    p_action_type varchar,
    p_entity_name varchar,
    p_entity_id int
) returns void as $$
begin
    insert into action_logs (user_id, action_type, entity_name, entity_id)
    values (p_user_id, p_action_type, p_entity_name, p_entity_id);
end;
$$ language plpgsql;

-- пример вызова функции 
select log_action(1, 'login', 'system_users', 1);

-- 2. автоматическое журналирование через триггер 

-- функция, которая срабатывает при изменении таблицы equipment

create or replace function trg_log_equipment_changes()
returns trigger as $$
declare
    v_action varchar;
    v_entity_id int;
begin
    v_action := lower(tg_op);

    if tg_op = 'delete' then
        v_entity_id := old.id;
    else
        v_entity_id := new.id;
    end if;

    perform log_action(1, v_action, 'equipment', v_entity_id);

    return new;
end;
$$ language plpgsql;

-- создание триггера
drop trigger if exists trg_equipment_log on equipment;
create trigger trg_equipment_log
after insert or update or delete on equipment
for each row execute function trg_log_equipment_changes();


-- меняем статус турникета
update equipment set status = 'renovation' where id = 1;

-- 4. проверяем результат: в логе должна появиться свежая запись с action_type = 'update'
select 
    al.timestamp, 
    u.login as user_login, 
    al.action_type, 
    al.entity_name, 
    al.entity_id
from action_logs al
left join system_users u on al.user_id = u.id
order by al.timestamp desc
limit 3;