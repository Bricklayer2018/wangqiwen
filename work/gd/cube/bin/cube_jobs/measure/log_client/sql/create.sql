set names utf8;
create database if not exists cube;
use cube;
create table if not exists log_client_stat(
    date varchar(20) not null,
    div0 varchar(50) not null,   
    page varchar(50) not null,
    button varchar(50) not null,
    pv int
);

-- exception values
-- insert into log_sp_stat values('-','-','-','-');
-- load data local infile 'data.txt' into table log_sp_stat;
-- delete from log_sp_stat where date='20140904'; 


