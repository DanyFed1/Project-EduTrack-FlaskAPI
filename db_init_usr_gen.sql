CREATE DATABASE fxmnd_task_10;
CREATE USER master_user WITH PASSWORD 'test_password_for_master_user';
GRANT ALL PRIVILEGES ON DATABASE fxmnd_task_10 TO master_user;
GRANT USAGE ON SCHEMA public TO master_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO master_user;
GRANT CREATE ON SCHEMA public TO master_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO master_user;