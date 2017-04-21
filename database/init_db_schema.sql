  -- sqlite3 mc_project13.db < init_db_schema.sql
  -- Create this

  drop table if exists users;
  create table users (
    id integer primary key autoincrement,
    name text,
    phone text,
    username text unique not null,
    email text unique not null,
    password not null
);