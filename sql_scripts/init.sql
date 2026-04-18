-- This script is used to initialize a MySQL database to be compatible with the script. It creates a new database called 'ds2500' in the MySQL server with the table below.

-- Create the database used in the MySQL databse to store the data.
CREATE DATABASE IF NOT EXISTS ds2500;

-- Create the properties table used for DS 2500 final project
CREATE TABLE IF NOT EXISTS ds2500.properties (
    rentcast_id VARCHAR(255) NOT NULL PRIMARY KEY,

    address VARCHAR(255) NOT NULL,
    state CHAR(2) NOT NULL,
    county CHAR(64) NOT NULL,
    city CHAR(64) NOT NULL,
    zip INT NOT NULL,

    sqft FLOAT NOT NULL,
    bedrooms FLOAT NOT NULL,
    bathrooms FLOAT NOT NULL,
    lot_size FLOAT NOT NULL,
    price FLOAT NOT NULL,

    year_built INT NOT NULL,
    listed_date DATE NOT NULL
);

