# Apache Spark Compute Engine
A standalone Apache Spark cluster (v4.2.0) for heavy data processing and ETL tasks.

## Components
* **Spark Master**: Coordinates the cluster resources (UI on Port 8083).
* **Spark Workers**: 2 worker nodes that execute the actual dataframe tasks (2 CPUs, 3GB RAM limit each).
* **History Server**: UI for viewing completed and historical Spark jobs (Port 18080).

## Customization & Security
* The custom Dockerfile injects Hadoop AWS v2, Delta Lake, and Iceberg JARs directly into the image.
* entrypoint.sh securely injects MinIO and Postgres credentials into spark-defaults.conf at runtime via sed, ensuring no plain-text passwords are leaked in source control.
