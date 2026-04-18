-- Create the database used in the MySQL databse to store the data.
CREATE DATABASE IF NOT EXISTS ds2500;

-- Create the houses table used for DS 2500 final project
CREATE TABLE IF NOT EXISTS ds2500.properties (
    rentcast_id VARCHAR(255) NOT NULL PRIMARY KEY,

    address VARCHAR(255) NOT NULL,
    state CHAR(2) NOT NULL,
    county CHAR(64) NOT NULL,
    city CHAR(64) NOT NULL,
    zip INT NOT NULL,

    sqft INT NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    lot_size INT NOT NULL,
    year_built INT NOT NULL,
    listing_date DATE NOT NULL
);

