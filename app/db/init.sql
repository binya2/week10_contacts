CREATE DATABASE IF NOT EXISTS rolling_project;

USE rolling_project;


CREATE TABLE IF NOT EXISTS user (
    id int,
    first_name varchar(50) DEFAULT NULL,
    last_name varchar(50) DEFAULT NULL,
    phone_number: varchar(50),
    PRIMARY KEY (id)
);