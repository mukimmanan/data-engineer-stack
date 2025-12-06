from pyspark.sql import SparkSession

# Define the full extensions string, ensuring only the Iceberg extension is active,
# since the default 'spark_catalog' is being configured as an Iceberg catalog.
EXTENSIONS = "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("IcebergTesting") \
    .getOrCreate()

# Create a sample DataFrame to write
data = spark.createDataFrame(
    [
        ("TSLA", 900.0, "2023-01-01"),
        ("GOOG", 150.0, "2023-01-02")
    ],
    ["ticker", "price", "date"]
)

spark.sql("CREATE DATABASE IF NOT EXISTS postgres_catalog.stocks")

# Now write to the Iceberg table using the default catalog.
data.writeTo("postgres_catalog.stocks.ice").createOrReplace()

spark.sql("SELECT * FROM postgres_catalog.stocks.ice").show()