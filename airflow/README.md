# Apache Airflow Orchestration
This directory contains the configuration for Apache Airflow, responsible for scheduling and orchestrating data pipelines.

## Components
* **Airflow Core Services**: Webserver, Scheduler, Triggerer, and Worker nodes running version 3.3.2.
* **Redis**: Used as the Celery backend for distributing tasks to workers.
* **Custom Image**: A custom Dockerfile installs necessary provider packages (Spark, MinIO, Docker, Hive) via equirements.txt.
* **Docker Proxy**: A secured socket proxy allowing Airflow to spawn Docker operators safely.

## Directories
* dags/: Place your DAG Python scripts here.
* plugins/: Custom Airflow plugins.
* config/: Airflow configuration file (irflow.cfg).
