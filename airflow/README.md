# Apache Airflow Orchestration
This directory contains the configuration for Apache Airflow, responsible for scheduling and orchestrating data pipelines.

## Components
* **Airflow Core Services**: Webserver, Scheduler, Triggerer, and Worker nodes running version 3.3.2.
* **Redis**: Used as the Celery backend for distributing tasks to workers.
* **Custom Image**: A custom Dockerfile installs necessary provider packages (Spark, MinIO, Docker, Hive) via requirements.txt.
* **Docker Proxy**: A secured socket proxy allowing Airflow to spawn Docker operators safely.

## Directories
* `dags/`: Place your DAG Python scripts here.
  * `daily_kafka_to_delta_dag.py`: Daily pipeline that triggers the Spark cluster streaming job to ingest Kafka financial transactions into Delta Lake (MinIO) via micro-batch upsert.
* `plugins/`: Custom Airflow plugins.
* `config/`: Airflow configuration file (`airflow.cfg`).
