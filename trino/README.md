# Trino Distributed Query Engine & Hive Metastore
Provides high-performance distributed SQL querying capabilities across the data lake using Trino (v483).

## Components
* **Hive Metastore**: (v4.0.1) Serves as the central metadata catalog for Iceberg, Delta, and traditional Hive tables stored in MinIO.
* **Trino Coordinator**: Parses, plans, and schedules SQL queries (UI on Port 8093).
* **Trino Worker**: Executes the query tasks.

## Catalogs
Configured in conf/coordinator/catalog/:
* minio.properties: Standard Hive connector pointing to MinIO.
* minio_iceberg.properties: Iceberg connector using the central Postgres database as the catalog.
* minio_delta.properties: Delta Lake native connector.

*Note: Passwords and keys are securely injected into these property files using Trino's native ${ENV:VAR} syntax.*
