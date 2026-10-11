import os
import sys
import time
import json
import urllib.request
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

def get_spark_session():
    """
    Initializes and returns a SparkSession with Delta Lake, Hive Metastore, and MinIO S3A configs.
    Connects to Hive Metastore so tables can be queried like AWS Glue & Athena.
    """
    minio_user = os.getenv("MINIO_ROOT_USER", "root_user")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "root_password")

    builder = (SparkSession.builder
        .appName("KafkaToDeltaStreamingUpsert")
        .enableHiveSupport()
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension,org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083")
        .config("spark.sql.warehouse.dir", "s3a://staging/databases/")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", minio_user)
        .config("spark.hadoop.fs.s3a.secret.key", minio_password)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.input.stream.type", "classic")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false"))

    return builder.getOrCreate()

def register_delta_table_in_trino(schema_name, table_name, table_location, trino_host="trino-coordinator", trino_port=8080):
    """
    Registers the Delta Lake table in Trino's minio_delta catalog (backed by Hive Metastore),
    enabling querying across the lakehouse just like AWS Glue Data Catalog and Athena.
    """
    url = f"http://{trino_host}:{trino_port}/v1/statement"
    query = f"CALL minio_delta.system.register_table(schema_name => '{schema_name}', table_name => '{table_name}', table_location => '{table_location}')"
    headers = {"X-Trino-User": "spark"}

    try:
        req = urllib.request.Request(url, data=query.encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        while "nextUri" in data:
            time.sleep(0.5)
            next_req = urllib.request.Request(data["nextUri"], headers=headers)
            with urllib.request.urlopen(next_req, timeout=10) as next_resp:
                data = json.loads(next_resp.read().decode("utf-8"))

        if "error" in data:
            err = data["error"].get("message", "")
            if "already exists" in err.lower():
                print(f"Table '{schema_name}.{table_name}' is already registered in Trino/Hive Metastore.")
            else:
                print(f"Trino registration notice: {err}")
        else:
            print(f"Successfully registered table '{schema_name}.{table_name}' in Trino/Hive Metastore.")
    except Exception as e:
        print(f"Trino registration notice: {e}")

def upsert_to_delta(micro_batch_df, batch_id):
    """
    Upserts each streaming micro-batch into the Delta table via path-based MERGE INTO
    and ensures the table is registered in Hive Metastore/Trino.
    """
    if micro_batch_df.rdd.isEmpty():
        print(f"[Batch {batch_id}] Micro-batch is empty. Skipping.")
        return

    record_count = micro_batch_df.count()
    print(f"[Batch {batch_id}] Ingesting {record_count} record(s) into Delta Lake...")

    # Flatten and deduplicate by transaction_id in this micro-batch
    cleaned_df = micro_batch_df.select(
        col("payload.transaction_id").alias("transaction_id"),
        col("payload.timestamp").alias("timestamp"),
        col("payload.amount").alias("amount"),
        col("payload.currency").alias("currency"),
        col("payload.merchant").alias("merchant"),
        col("payload.transaction_type").alias("transaction_type"),
        col("payload.is_flagged_fraud").alias("is_flagged_fraud"),
        col("payload.device_type").alias("device_type"),
        col("payload.user.user_id").alias("user_id"),
        col("payload.user.full_name").alias("user_full_name"),
        col("payload.user.email").alias("user_email"),
        col("payload.user.ip_address").alias("user_ip"),
        col("payload.location.country").alias("country"),
        col("payload.location.city").alias("city"),
        col("payload.location.latitude").alias("latitude"),
        col("payload.location.longitude").alias("longitude"),
        col("kafka_timestamp")
    ).filter("transaction_id IS NOT NULL").dropDuplicates(["transaction_id"])

    spark = micro_batch_df.sparkSession
    db_name = "lakehouse"
    table_name = "financial_transactions"
    delta_target_path = f"s3a://staging/databases/{db_name}.db/{table_name}"
    delta_table_identifier = f"delta.`{delta_target_path}`"

    try:
        spark.read.format("delta").load(delta_target_path).take(1)
        table_exists = True
    except Exception:
        table_exists = False

    if table_exists:
        cleaned_df.createOrReplaceTempView("batch_updates")
        spark.sql(f"""
            MERGE INTO {delta_table_identifier} AS target
            USING batch_updates AS source
            ON target.transaction_id = source.transaction_id
            WHEN MATCHED THEN UPDATE SET *
            WHEN NOT MATCHED THEN INSERT *
        """)
        print(f"[Batch {batch_id}] Successfully upserted (MERGE) into Delta path '{delta_target_path}'.")
    else:
        print(f"[Batch {batch_id}] Initializing Delta table at {delta_target_path}...")
        (cleaned_df.write
            .format("delta")
            .mode("overwrite")
            .save(delta_target_path))
        print(f"[Batch {batch_id}] Successfully initialized Delta table at {delta_target_path}.")
        register_delta_table_in_trino(db_name, table_name, delta_target_path)

def main():
    print("=" * 60)
    print("Starting Spark Streaming Kafka to Delta Lake Upsert Job")
    print("=" * 60)

    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    kafka_bootstrap_servers = "kafka-0:29092,kafka-1:29092,kafka-2:29092"
    topic_name = "global_financial_transactions"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    desc_file_path = os.getenv("PROTO_DESC_PATH", os.path.join(script_dir, "transaction.desc"))
    if not os.path.exists(desc_file_path):
        desc_file_path = "/notebooks/daily_kafka_to_delta_spark_job/transaction.desc"
    checkpoint_path = "s3a://staging/delta/checkpoints/financial_transactions"
    db_name = "lakehouse"
    table_name = "financial_transactions"
    delta_target_path = f"s3a://staging/databases/{db_name}.db/{table_name}"

    print(f"Subscribing to Kafka Topic: {topic_name} at {kafka_bootstrap_servers}")
    kafka_stream = (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", topic_name)
        .option("startingOffsets", "earliest")
        .load())

    # Strip Confluent Protobuf wire format header:
    # 1 byte magic + 4 bytes schema ID + 2 bytes message index = 7 bytes.
    # SQL substring is 1-based, so substring(value, 8) extracts the raw Protobuf binary.
    raw_payload_df = kafka_stream.select(
        col("key").cast("string").alias("kafka_key"),
        col("timestamp").alias("kafka_timestamp"),
        expr("substring(value, 8)").alias("raw_protobuf")
    )

    try:
        from pyspark.sql.protobuf.functions import from_protobuf
        with open(desc_file_path, "rb") as f:
            desc_bytes = f.read()

        parsed_df = raw_payload_df.select(
            col("kafka_key"),
            col("kafka_timestamp"),
            from_protobuf(
                col("raw_protobuf"),
                "finance.Transaction",
                binaryDescriptorSet=desc_bytes,
                options={"mode": "PERMISSIVE"}
            ).alias("payload")
        )
    except Exception as e:
        print(f"Warning: Could not load spark-protobuf function ({e}). Processing without protobuf schema.")
        sys.exit(1)

    print("Configuring Structured Streaming writer with Delta upsert and Trigger.AvailableNow...")
    query = (parsed_df.writeStream
        .format("delta")
        .foreachBatch(upsert_to_delta)
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .start())

    print("Waiting for micro-batch stream execution to complete...")
    query.awaitTermination()

    # Ensure table registration in Trino/Hive Metastore post-job
    register_delta_table_in_trino(db_name, table_name, delta_target_path)

    print("=" * 60)
    print("Spark Streaming Job Finished Successfully! Table available in Hive Metastore and Trino.")
    print("=" * 60)

if __name__ == "__main__":
    main()
