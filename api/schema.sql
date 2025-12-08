create table if not exists speakers (
    id integer primary key AUTOINCREMENT,
    conferenceId text not null, 
    firstname text not null, 
    lastname text not null, 
    email text,
    phone text,
    profilepic text,
    bio text
);

create table if not exists talks (
    id integer primary key AUTOINCREMENT, 
    title text, 
    description text, 
    speaker integer not null
);

CREATE TABLE if not exists conferences (
    conferenceId TEXT PRIMARY KEY COLLATE NOCASE
);

create table if not exists sponsors(
    id integer primary key AUTOINCREMENT,
    conferenceId text,
    name text not null,
    logo text,
    url text,
    level text
);