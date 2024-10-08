DROP DATABASE IF EXISTS qqh_problems;
CREATE DATABASE qqh_problems;

USE qqh_problems;

CREATE TABLE betting_bankrolls(
    id INT auto_increment,
    bet_date DATE,
    user_id INT,
    cash FLOAT,
    cash_invested FLOAT,
    primary key(id)
);

