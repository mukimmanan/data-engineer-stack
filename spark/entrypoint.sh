#!/bin/bash
set -e

ROLE=${SPARK_ROLE}

# Ensure eventlog directory exists with proper permissions
mkdir -p /eventlog
chmod 777 /eventlog

if [ "$ROLE" = "master" ]; then
  exec /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master \
    --host 0.0.0.0 \
    --port 7077 \
    --webui-port 8080
elif [ "$ROLE" = "worker" ]; then
  exec /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker \
    spark://spark-master:7077 \
    --webui-port 8081
elif [ "$ROLE" = "history" ]; then
  exec /opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer
else
  echo "Unknown SPARK_ROLE: $ROLE"
  exit 1
fi
