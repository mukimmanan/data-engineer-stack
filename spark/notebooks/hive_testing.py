from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("HiveTesting") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .enableHiveSupport() \
    .getOrCreate()


# spark.sql("DROP TABLE IF EXISTS stocks.testing_hive_table3")

spark.sql("SHOW DATABASES").show()
spark.sql("USE stocks")

data = spark.sql("SHOW DATABASES")


# data.write.mode("overwrite").saveAsTable("stocks.testing_parquet")
# data.write.mode("overwrite").format("csv").option("header", "true").saveAsTable("stocks.testing_csv")
data.write.mode("overwrite").option("truncate", "true").format("delta").saveAsTable("stocks.delta")

# spark.sql("SELECT * FROM stocks.testing_parquet").show()
# spark.sql("SELECT * FROM stocks.testing_csv").show()
spark.sql("SELECT * FROM stocks.delta").show()