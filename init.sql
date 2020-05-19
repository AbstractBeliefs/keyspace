drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null unique,
    password text not null
);

drop table if exists keys;
create table keys (
    id integer primary key autoincrement,
    owner integer not null,
    fingerprint text not null,
    key blob not null
);

drop table if exists verifications;
create table verifications (
    id integer primary key autoincrement,
    key integer not null,
    driver text not null,
    data text not null,
    last_checked datetime,
    valid boolean
);
