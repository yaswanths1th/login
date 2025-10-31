-- db_setup.sql
-- Create the database and tables for local testing. Adjust names/credentials as needed.

-- 1) Create database (run as postgres user)
-- CREATE DATABASE otp_demo_db;

-- 2) Create user (optional)
-- CREATE USER postgres WITH PASSWORD 'postgres';

-- 3) Grant privileges (if you created a new DB/user)
-- GRANT ALL PRIVILEGES ON DATABASE otp_demo_db TO postgres;

-- 4) Table creation (if you prefer to create tables manually; migrations will automatically create these, but here's SQL)
CREATE TABLE IF NOT EXISTS accounts_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts_otpcode (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    expiry_time TIMESTAMP WITHOUT TIME ZONE NOT NULL
);
