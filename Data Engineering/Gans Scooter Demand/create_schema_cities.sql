-- Drop the database if it already exists
DROP DATABASE IF EXISTS cities;

-- Create the database
CREATE DATABASE cities;

-- Use the database
USE cities;

-- Create the 'city' table
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT, -- Automatically generated ID for each city
    city_name VARCHAR(255) NOT NULL, -- Name of the city
    country VARCHAR(255) NOT NULL, -- Country of the City
    longitude FLOAT(8,6), -- City Coordinates
    latitude FLOAT(8,6), -- City  Coordinates
    PRIMARY KEY (city_id) -- Primary key to uniquely identify each city
);

-- Create the 'population' table
CREATE TABLE population (
    population_id INT AUTO_INCREMENT, -- Automatically generated ID for each population entry
    city_id INT, -- city_ID to cross-reference
    population INT, -- population at the time of assessment
    date_fetched DATETIME, -- date of the assessment
    PRIMARY KEY (population_id), -- Primary key to uniquely identify each population entry
    FOREIGN KEY (city_id) REFERENCES cities(city_id) -- Foreign key to connect population to city
);

-- Create the 'forecast' table
CREATE TABLE forecast (
    forecast_id INT AUTO_INCREMENT, -- Automatically generated ID for each forecast entry
    city_id INT, -- ID of the city
    forecast_time DATETIME, -- datetime of forecast
    outlook VARCHAR(255), --  description of weather forecast
    temp FLOAT, -- temperatur in °C
    feels_like FLOAT, -- perceived temperature 
    wind_speed FLOAT, -- wind speed in m/s
    rain_3h FLOAT, -- rain in mm over 3h
    date_fetched DATETIME, -- datetime, when forecast was fetched
    PRIMARY KEY (forecast_id), -- Primary key to uniquely identify each population entry
    FOREIGN KEY (city_id) REFERENCES cities(city_id) -- Foreign key to connect each forecast to its city
);

-- Create the 'airports' table
CREATE TABLE airports (
    icao_code VARCHAR(4), -- ICAO Code of Airport
    iata_code VARCHAR(3), -- IATA Code of Airport
    full_name VARCHAR(50), -- full Airport name
    latitude FLOAT(8,6), -- airport coordinates
    longitude FLOAT(8,6), -- airport coordinates
    country_code VARCHAR(2), -- Country Code
    PRIMARY KEY (icao_code) -- define unique identifier
);

-- Create the 'cities_airports' table - it sits between 'cities' and 'airports' as an intermediate in a many-to-many relationship
CREATE TABLE cities_airports (
    icao_code VARCHAR(4), -- ICEA Code of Airport
    city_id INT, -- ID of the city
     -- no primary key, as there might be several airport for on city and several cities for on airport
    FOREIGN KEY (city_id) REFERENCES cities(city_id), -- Foreign key to connect each info to its city
    FOREIGN KEY (icao_code) REFERENCES airports(icao_code) -- Foreign key to connect each info to its city
);

-- Create the 'arrivals' table
CREATE TABLE arrivals (
    arrivals_id INT AUTO_INCREMENT, -- Automatically generated ID for each entry
    arrival_airport_icao VARCHAR(4),
    departure_airport_icao VARCHAR(4),
    departure_airport_name VARCHAR(50),
    departure_scheduledTime_local DATETIME,
    arrival_scheduledTime_local DATETIME,
    arrival_revisedTime_local DATETIME,
    aircraft_model VARCHAR(50),
    airline_name VARCHAR(50),
    date_fetched DATETIME,
    PRIMARY KEY (arrivals_id), -- Primary key to uniquely identify each population entry
    FOREIGN KEY (arrival_airport_icao) REFERENCES airports(icao_code) -- Foreign key to connect each info to its city
);