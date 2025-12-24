CREATE DATABASE IF NOT EXISTS rolling_project;

USE rolling_project;

CREATE TABLE IF NOT EXISTS contacts (
    id int NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    phone_number varchar(20) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO contacts (first_name, last_name, phone_number) VALUES
    ('John', 'Doe', '050-1234567'),
    ('Jane', 'Smith', '052-9876543'),
    ('Bob', 'Johnson', '054-5555555'),
    ('Jack', 'Robinson', '050-6115555');