#!/bin/bash
# --- Configuration ---
SPARK_VERSION="4.0.1"
HADOOP_VERSION="3"
SPARK_DIR="/opt/spark"

# Define Download URL
SPARK_TGZ="spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"
SPARK_URL="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/${SPARK_TGZ}"

# --- Installation Steps ---

echo "Starting download of Spark ${SPARK_VERSION} client..."

# Download and check for success
wget -q ${SPARK_URL} -O /tmp/${SPARK_TGZ}
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to download Spark client from ${SPARK_URL}"
    exit 1
fi

# Extract and cleanup
tar -xzf /tmp/${SPARK_TGZ} -C /opt/
rm /tmp/${SPARK_TGZ}

# Rename the extracted folder to a clean, expected path (/opt/spark)
mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_DIR}

echo "Spark client installed successfully at ${SPARK_DIR}"
