#!/bin/bash
set -e

# Use the first command-line argument ($1) as the role, 
# falling back to SPARK_ROLE if $1 is empty.
# This makes it compatible with both "docker run --env SPARK_ROLE=master" 
# and "command: [zeppelin, ...]"
ROLE=${1:-$SPARK_ROLE}

# Ensure eventlog directory exists with proper permissions
mkdir -p /eventlog
chmod 777 /eventlog

# --- Check for Zeppelin Role ---
if [ "$ROLE" = "zeppelin" ]; then
    echo "Launching Apache Zeppelin..."
    
    # Ensure necessary environment variables are set explicitly
    export ZEPPELIN_HOME=/opt/zeppelin
    export SPARK_HOME=/opt/spark
    
    # CRITICAL: Shift the arguments to remove 'zeppelin' and execute the rest.
    # The remaining arguments are: "zeppelin-daemon.sh", "start"
    shift
    
    # Execute the remaining command and replace the shell process
    exec "$@"

# --- Check for Spark Roles ---
elif [ "$ROLE" = "master" ]; then
    echo "Launching Spark Master..."
    exec /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master \
        --host 0.0.0.0 \
        --port 7077 \
        --webui-port 8080
elif [ "$ROLE" = "worker" ]; then
    echo "Launching Spark Worker..."
    exec /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker \
        spark://spark-master:7077 \
        --webui-port 8081
elif [ "$ROLE" = "history" ]; then
    echo "Launching Spark History Server..."
    exec /opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer
else
    echo "Unknown/Missing Role or Command: $ROLE"
    echo "Available roles: master, worker, history, zeppelin"
    exit 1
fi