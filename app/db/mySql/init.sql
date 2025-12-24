create DATABASE IF NOT EXISTS rolling_project;

USE rolling_project;


create TABLE IF NOT EXISTS contacts (
    id int NOT NULL AUTO_INCREMENT,
    first_name varchar(50) DEFAULT NULL,
    last_name varchar(50) DEFAULT NULL,
    phone_number varchar(50),
    PRIMARY KEY (id)
);