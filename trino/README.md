# Trino Distributed Query Engine & Hive Metastore
Provides high-performance distributed SQL querying capabilities across the data lake using Trino (v483).

## Components
* **Hive Metastore**: (v4.0.1) Serves as the central metadata catalog for Iceberg, Delta, and traditional Hive tables stored in MinIO.
* **Trino Coordinator**: Parses, plans, and schedules SQL queries (Cluster Monitoring UI on Port 8093).
* **Trino Worker**: Executes the query tasks.
* **Trino Query UI (CloudBeaver)**: Web-based SQL query editor and database workbench for querying Trino (Interactive Query UI on Port 8978).

## Catalogs
Configured in conf/coordinator/catalog/:
* minio.properties: Standard Hive connector pointing to MinIO.
* minio_iceberg.properties: Iceberg connector using the central Postgres database as the catalog.
* minio_delta.properties: Delta Lake native connector.

*Note: Passwords and keys are securely injected into these property files using Trino's native ${ENV:VAR} syntax.*

