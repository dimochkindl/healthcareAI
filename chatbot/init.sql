-- Connect to the database (if needed)
-- This step is optional if the database is already selected
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'giga') THEN
        CREATE DATABASE giga;
    END IF;
END $$;

-- Connect to the 'giga' database
\c giga;

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
