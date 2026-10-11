#!/bin/bash
set -e

# Use the first command-line argument ($1) as the role, 
# falling back to SPARK_ROLE if $1 is empty.
# This makes it compatible with both "docker run --env SPARK_ROLE=master" 
# and "command: [zeppelin, ...]"
ROLE=${1:-$SPARK_ROLE}

# Ensure eventlog directory exists with proper permissions
mkdir -p /eventlog 2>/dev/null || true
chmod 777 /eventlog 2>/dev/null || true
mkdir -p /tmp/spark-events 2>/dev/null || true

# Safely inject environment variables into spark-defaults.conf at container boot
if [ -f /opt/spark/conf/spark-defaults.conf ]; then
    sed -i "s/\${MINIO_ROOT_USER}/${MINIO_ROOT_USER:-root_user}/g" /opt/spark/conf/spark-defaults.conf 2>/dev/null || true
    sed -i "s/\${MINIO_ROOT_PASSWORD}/${MINIO_ROOT_PASSWORD:-root_password}/g" /opt/spark/conf/spark-defaults.conf 2>/dev/null || true
    sed -i "s/\${POSTGRES_PASSWORD}/${POSTGRES_PASSWORD:-iceberg}/g" /opt/spark/conf/spark-defaults.conf 2>/dev/null || true
    grep -q "spark.hadoop.fs.s3a.input.stream.type" /opt/spark/conf/spark-defaults.conf 2>/dev/null || echo "spark.hadoop.fs.s3a.input.stream.type classic" >> /opt/spark/conf/spark-defaults.conf
fi

# --- Check for Zeppelin Role ---
if [ "$ROLE" = "zeppelin" ]; then
    echo "Launching Apache Zeppelin..."
    
    # Ensure necessary environment variables are set explicitly
    export ZEPPELIN_HOME=/opt/zeppelin
    export SPARK_HOME=/opt/spark
    
    # Seed interpreter.json from mounted seed file if provided
    if [ -f /opt/zeppelin/conf_seed/interpreter.json ]; then
        cp -f /opt/zeppelin/conf_seed/interpreter.json /opt/zeppelin/conf/interpreter.json 2>/dev/null || true
        chmod 666 /opt/zeppelin/conf/interpreter.json 2>/dev/null || true
    fi

    # Ensure Trino JDBC driver is present for %trino interpreter
    if ! ls /opt/zeppelin/interpreter/jdbc/trino-jdbc-*.jar 1>/dev/null 2>&1; then
        echo "Downloading Trino JDBC driver for Zeppelin..."
        curl -f -L --retry 3 -o /opt/zeppelin/interpreter/jdbc/trino-jdbc-438.jar \
            https://repo1.maven.org/maven2/io/trino/trino-jdbc/438/trino-jdbc-438.jar 2>/dev/null || true
    fi

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