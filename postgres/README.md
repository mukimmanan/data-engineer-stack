# PostgreSQL Central Metadata Store
This single PostgreSQL instance (v16.15) serves as the backbone for multiple services across the stack.

## Databases
Provisioned automatically via init-databases.sql:
* irflow: Metadata backend for Apache Airflow.
* metastore: Backend for the Hive Metastore.
* iceberg_db: Catalog database for Apache Iceberg.
* cdc_db: A sample database configured for testing Debezium CDC (contains a sample orders table).
* conduktor_db: State storage for the Conduktor Console UI.

## CDC Configuration
The database is booted with command: postgres -c wal_level=logical. This is strictly required to allow Debezium to read the Write-Ahead Logs (WAL) for Change Data Capture.
