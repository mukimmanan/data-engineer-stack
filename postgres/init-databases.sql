CREATE USER airflow WITH PASSWORD 'airflow';
CREATE USER hive WITH PASSWORD 'hive';
CREATE USER main WITH PASSWORD 'main';
CREATE USER iceberg WITH PASSWORD 'iceberg';

CREATE DATABASE airflow OWNER airflow;
CREATE DATABASE hive OWNER hive;
CREATE DATABASE data_warehouse OWNER main;
CREATE DATABASE iceberg_db OWNER iceberg;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;
GRANT ALL PRIVILEGES ON DATABASE data_warehouse TO main;
GRANT ALL PRIVILEGES ON DATABASE iceberg_db TO iceberg;
-- Database for Debezium CDC Demo
CREATE DATABASE cdc_db;
\c cdc_db
CREATE TABLE IF NOT EXISTS public.orders (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Configure replication privileges
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;

-- Database for Conduktor Console State
CREATE DATABASE conduktor_db;
CREATE USER conduktor WITH PASSWORD 'conduktor_pass';
GRANT ALL PRIVILEGES ON DATABASE conduktor_db TO conduktor;
