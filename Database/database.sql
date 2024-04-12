CREATE TABLE users(
id SERIAL primary KEY,
firstname varchar(100) not null,
lastname varchar(100) not null,
email varchar(255) unique not null,
password varchar(255) not null);