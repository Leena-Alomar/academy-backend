CREATE DATABASE academy;

CREATE USER academy_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE academy TO academy_admin;
