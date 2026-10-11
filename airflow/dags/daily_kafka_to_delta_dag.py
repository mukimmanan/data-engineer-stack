"""
Airflow DAG: Daily Kafka to Delta Lake Spark Streaming Upsert Job
Schedule: Once a day (@daily)
Description:
    Triggers a Spark Structured Streaming job on the Spark Master cluster.
    The job reads Protobuf-serialized messages from Kafka ('global_financial_transactions'),
    decodes them, and performs a micro-batch UPSERT (MERGE) into Delta Lake in MinIO (s3a://staging/delta/financial_transactions).
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta

# Modern Airflow 3 TaskFlow SDK with fallback to classic decorator imports
try:
    from airflow.sdk import dag, task
    from airflow.sdk.exceptions import AirflowException
except ImportError:
    from airflow.decorators import dag, task  # type: ignore[no-redef]
    from airflow.exceptions import AirflowException  # type: ignore[no-redef]

import docker

logger = logging.getLogger("airflow.task")

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="daily_kafka_to_delta_spark_job",
    dag_display_name="Daily Kafka to Delta Lake Spark Streaming Upsert",
    description="Triggers daily Spark streaming job to upsert Kafka financial transactions into Delta Lake (MinIO)",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["spark", "kafka", "delta", "streaming", "minio"],
    doc_md=__doc__,
)
def daily_kafka_to_delta_spark_pipeline():
    @task(
        task_id="trigger_spark_kafka_to_delta_upsert",
        execution_timeout=timedelta(hours=2),
    )
    def execute_spark_job_on_cluster() -> None:
        """
        Connects to the Docker proxy socket and executes spark-submit inside
        the spark-master container, streaming logs in real-time.
        """
        docker_proxy_url = "tcp://docker-proxy:2375"
        target_container_name = "spark-master"
        spark_script_path = "/notebooks/daily_kafka_to_delta_spark_job/stream_kafka_to_delta.py"

        logger.info("Connecting to Docker daemon via %s...", docker_proxy_url)
        client = docker.DockerClient(base_url=docker_proxy_url)

        try:
            container = client.containers.get(target_container_name)
        except docker.errors.NotFound:
            raise AirflowException(f"Container '{target_container_name}' not found on Docker network!")

        spark_submit_cmd = [
            "/opt/spark/bin/spark-submit",
            "--master", "spark://spark-master:7077",
            "--deploy-mode", "client",
            "--name", "Airflow_Daily_Kafka_to_Delta_Upsert",
            "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0,org.apache.spark:spark-protobuf_2.13:4.2.0",
            spark_script_path,
        ]

        logger.info("=" * 60)
        logger.info("Submitting Spark job to %s:", target_container_name)
        logger.info(" ".join(spark_submit_cmd))
        logger.info("=" * 60)

        # Use low-level client API for streaming and inspecting exit code
        exec_created = client.api.exec_create(
            container=container.id,
            cmd=spark_submit_cmd,
            stdout=True,
            stderr=True,
        )
        exec_id = exec_created["Id"]

        output_stream = client.api.exec_start(exec_id, stream=True)
        for chunk in output_stream:
            if chunk:
                decoded = chunk.decode("utf-8", errors="replace")
                sys.stdout.write(decoded)
                sys.stdout.flush()

        # Inspect the execution exit code
        exec_info = client.api.exec_inspect(exec_id)
        exit_code = exec_info.get("ExitCode")

        logger.info("Spark Job Exit Code: %s", exit_code)
        if exit_code != 0:
            raise AirflowException(f"Spark job in {target_container_name} failed with exit code {exit_code}")

        logger.info("Spark Streaming Kafka to Delta Lake job completed successfully!")

    execute_spark_job_on_cluster()


# Instantiate DAG for Airflow DAG discovery
daily_kafka_to_delta_spark_pipeline()
