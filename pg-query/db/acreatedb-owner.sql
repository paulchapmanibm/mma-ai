-- Create database owner/role
CREATE ROLE rentalco WITH LOGIN PASSWORD 'rentalco';

-- Create the database with the owner
CREATE DATABASE rentalco WITH OWNER = rentalco;

-- Connect to the new database
\c rentalco

-- Set default privileges for the owner
ALTER DEFAULT PRIVILEGES FOR ROLE rentalco IN SCHEMA public
GRANT ALL ON TABLES TO rentalco;

ALTER DEFAULT PRIVILEGES FOR ROLE rentalco IN SCHEMA public
GRANT ALL ON SEQUENCES TO rentalco;

