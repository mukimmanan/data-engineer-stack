"""
Airflow DAG: Daily Kafka to Delta Lake Spark Streaming Upsert Job
Schedule: Once a day (@daily)
Description:
    Triggers a Spark Structured Streaming job on the Spark Master cluster.
    The job reads Protobuf-serialized messages from Kafka ('global_financial_transactions'),
    decodes them, and performs a micro-batch UPSERT (MERGE) into Delta Lake in MinIO (s3a://staging/delta/financial_transactions).
"""

from datetime import datetime, timedelta
from airflow import DAG
try:
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.python import PythonOperator
import docker
import sys

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def execute_spark_job_on_cluster(**context):
    """
    Connects to the Docker proxy socket and executes spark-submit inside
    the spark-master container, streaming logs in real-time.
    """
    docker_proxy_url = "tcp://docker-proxy:2375"
    target_container_name = "spark-master"
    spark_script_path = "/notebooks/stream_kafka_to_delta.py"

    print(f"Connecting to Docker daemon via {docker_proxy_url}...")
    client = docker.DockerClient(base_url=docker_proxy_url)

    try:
        container = client.containers.get(target_container_name)
    except docker.errors.NotFound:
        raise RuntimeError(f"Container '{target_container_name}' not found on Docker network!")

    spark_submit_cmd = [
        "/opt/spark/bin/spark-submit",
        "--master", "spark://spark-master:7077",
        "--deploy-mode", "client",
        "--name", "Airflow_Daily_Kafka_to_Delta_Upsert",
        "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0,org.apache.spark:spark-protobuf_2.13:4.2.0",
        spark_script_path
    ]

    print("=" * 60)
    print(f"Submitting Spark job to {target_container_name}:")
    print(" ".join(spark_submit_cmd))
    print("=" * 60)

    # Execute command and stream output
    exec_instance = container.exec_run(
        cmd=spark_submit_cmd,
        stdout=True,
        stderr=True,
        stream=True
    )

    for chunk in exec_instance.output:
        if chunk:
            sys.stdout.write(chunk.decode("utf-8", errors="replace"))
            sys.stdout.flush()

    # Inspect the execution exit code
    exec_info = container.client.api.exec_inspect(exec_instance.exec_id)
    exit_code = exec_info.get("ExitCode")

    print(f"\nSpark Job Exit Code: {exit_code}")
    if exit_code != 0:
        raise RuntimeError(f"Spark job in {target_container_name} failed with exit code {exit_code}")

    print("Spark Streaming Kafka to Delta Lake job completed successfully!")

with DAG(
    dag_id='daily_kafka_to_delta_spark_job',
    default_args=default_args,
    description='Triggers daily Spark streaming job to upsert Kafka financial transactions into Delta Lake (MinIO)',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['spark', 'kafka', 'delta', 'streaming', 'minio']
) as dag:

    trigger_spark_job = PythonOperator(
        task_id='trigger_spark_kafka_to_delta_upsert',
        python_callable=execute_spark_job_on_cluster,
        execution_timeout=timedelta(hours=2)
    )

    trigger_spark_job
