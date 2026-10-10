import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from delta.tables import DeltaTable

def get_spark_session():
    """Initializes and returns a SparkSession with Delta Lake and MinIO S3A configs."""
    minio_user = os.getenv("MINIO_ROOT_USER", "admin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "password")

    builder = (SparkSession.builder
        .appName("KafkaToDeltaStreamingUpsert")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", minio_user)
        .config("spark.hadoop.fs.s3a.secret.key", minio_password)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false"))

    return builder.getOrCreate()

def upsert_to_delta(micro_batch_df, batch_id):
    """Upserts each streaming micro-batch into the Delta table in MinIO."""
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
    delta_target_path = "s3a://staging/delta/financial_transactions"

    if DeltaTable.isDeltaTable(spark, delta_target_path):
        delta_table = DeltaTable.forPath(spark, delta_target_path)
        (delta_table.alias("target")
            .merge(
                cleaned_df.alias("source"),
                "target.transaction_id = source.transaction_id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute())
        print(f"[Batch {batch_id}] Successfully upserted (MERGE) into Delta table at {delta_target_path}.")
    else:
        print(f"[Batch {batch_id}] Delta table not found at {delta_target_path}. Initializing new Delta table...")
        cleaned_df.write.format("delta").mode("overwrite").save(delta_target_path)
        print(f"[Batch {batch_id}] Delta table initialized at {delta_target_path}.")

def main():
    print("=" * 60)
    print("Starting Spark Streaming Kafka to Delta Lake Upsert Job")
    print("=" * 60)

    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    kafka_bootstrap_servers = "kafka-0:29092,kafka-1:29092,kafka-2:29092"
    topic_name = "global_financial_transactions"
    desc_file_path = "/notebooks/transaction.desc"
    checkpoint_path = "s3a://staging/delta/checkpoints/financial_transactions"

    print(f"Subscribing to Kafka Topic: {topic_name} at {kafka_bootstrap_servers}")
    kafka_stream = (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", topic_name)
        .option("startingOffsets", "earliest")
        .load())

    # Confluent Schema Registry prepends a 5-byte header (1 magic byte + 4 bytes schema ID).
    # We strip the first 5 bytes using substring(value, 6, length(value)-5) to obtain pure Protobuf binary.
    raw_payload_df = kafka_stream.select(
        col("key").cast("string").alias("kafka_key"),
        col("timestamp").alias("kafka_timestamp"),
        expr("substring(value, 6, length(value) - 5)").alias("raw_protobuf")
    )

    try:
        from pyspark.sql.protobuf.functions import from_protobuf
        parsed_df = raw_payload_df.select(
            col("kafka_key"),
            col("kafka_timestamp"),
            from_protobuf(col("raw_protobuf"), "finance.Transaction", descFilePath=desc_file_path).alias("payload")
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
    print("=" * 60)
    print("Spark Streaming Job Finished Successfully! All records ingested into Delta Lake.")
    print("=" * 60)

if __name__ == "__main__":
    main()
