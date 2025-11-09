create database library_db
create schema library

create table library.books(
book_id serial primary key,
title varchar(50) not null,
author varchar(50) unique,
published_year int,
available_copies int default 0,
created_at timestamp default now()
)

create table library.members(
member_id serial primary key,
name varchar(50) not null,
email varchar(50) not null,
phone varchar(11),
membership_date date default current_date
);


create table library.loans(
loan_id serial Primary Key,
book_id int references library.books(book_id),
member_id int references library.members(member_id),
loan_date DATE DEFAULT CURRENT_DATE,
due_date DATE NOT NULL,
return_date DATE NULL,
status VARCHAR(15) CHECK (status IN ('active', 'returned', 'overdue'))
);

