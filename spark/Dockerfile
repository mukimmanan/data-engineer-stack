FROM apache/spark:4.2.0

USER root

# ============================================================
# System dependencies — single consolidated layer
# ============================================================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl unzip wget net-tools procps && \
    rm -rf /var/lib/apt/lists/*

# ============================================================
# JAR Dependencies — Hadoop AWS, Delta, Iceberg
# ============================================================
# Spark 4.2.0 bundles Hadoop 3.5.0 — match hadoop-aws version
ARG HADOOP_AWS_VERSION=3.5.0

# Hadoop 3.5.0 S3A uses AWS SDK v2; no need for v1 bundle
ARG AWS_SDK_VERSION=2.39.5

# Delta Lake 4.2.0 for Spark 4.2
ARG DELTA_VERSION=4.2.0

# Iceberg 1.12.0 with Spark 4.2 runtime
ARG ICEBERG_VERSION=1.12.0

# PostgreSQL JDBC driver
ARG PG_DRIVER_VERSION=42.7.3

RUN mkdir -p /opt/spark/jars && \
    # Hadoop AWS (S3A filesystem)
    curl -f -L -o /opt/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    # AWS SDK v2 bundle (required by Hadoop 3.5.0 S3A)
    curl -f -L -o /opt/spark/jars/aws-sdk-bundle-${AWS_SDK_VERSION}.jar \
        https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar && \
    # HTTP client (S3A dependency)
    curl -f -L -o /opt/spark/jars/httpclient-4.5.14.jar \
        https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.14/httpclient-4.5.14.jar && \
    # Delta Lake
    curl -f -L -o /opt/spark/jars/delta-spark_2.13-${DELTA_VERSION}.jar \
        https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/${DELTA_VERSION}/delta-spark_2.13-${DELTA_VERSION}.jar && \
    curl -f -L -o /opt/spark/jars/delta-storage-${DELTA_VERSION}.jar \
        https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    # Apache Iceberg
    curl -f -L -o /opt/spark/jars/iceberg-spark-runtime-4.2_2.13-${ICEBERG_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.2_2.13/${ICEBERG_VERSION}/iceberg-spark-runtime-4.2_2.13-${ICEBERG_VERSION}.jar && \
    # PostgreSQL JDBC
    curl -f -L -o /opt/spark/jars/postgresql-${PG_DRIVER_VERSION}.jar \
        https://jdbc.postgresql.org/download/postgresql-${PG_DRIVER_VERSION}.jar && \
    echo "All JARs downloaded successfully"

# ============================================================
# Spark configuration
# ============================================================
COPY conf/ /opt/spark/conf/

# ============================================================
# Hive Metastore client JARs
# ============================================================
COPY ./hive_jars_401.sh /hive_jars.sh
RUN chmod +x /hive_jars.sh && /hive_jars.sh

# ============================================================
# Zeppelin (optional notebook server)
# ============================================================
ARG ZEPPELIN_VERSION=0.12.0
ENV ZEPPELIN_HOME=/opt/zeppelin
ENV ZEPPELIN_PACKAGE=zeppelin-${ZEPPELIN_VERSION}-bin-all
ENV ZEPPELIN_DOWNLOAD_URL=https://dlcdn.apache.org/zeppelin/zeppelin-${ZEPPELIN_VERSION}/${ZEPPELIN_PACKAGE}.tgz

RUN curl -f -L -o /tmp/zeppelin.tgz ${ZEPPELIN_DOWNLOAD_URL} && \
    mkdir -p ${ZEPPELIN_HOME} && \
    tar -xf /tmp/zeppelin.tgz -C /opt/ && \
    mv /opt/${ZEPPELIN_PACKAGE} ${ZEPPELIN_HOME} && \
    rm /tmp/zeppelin.tgz

RUN mv ${ZEPPELIN_HOME}/${ZEPPELIN_PACKAGE}/* ${ZEPPELIN_HOME}/ && \
    rm -rf ${ZEPPELIN_HOME}/${ZEPPELIN_PACKAGE}

RUN mkdir -p ${ZEPPELIN_HOME}/logs ${ZEPPELIN_HOME}/run ${ZEPPELIN_HOME}/notebook

# ============================================================
# Environment variables
# ============================================================
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$SPARK_HOME/bin:$ZEPPELIN_HOME/bin:$PATH

ENV ZEPPELIN_JMX_ENABLE=false
ENV ZEPPELIN_JAVA_OPTS="--add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"

# ============================================================
# Permissions — give ownership to 'spark' user (UID 185)
# ============================================================
RUN chown -R 185:0 ${ZEPPELIN_HOME} && \
    chmod -R g+w ${ZEPPELIN_HOME}

# ============================================================
# Entrypoint
# ============================================================
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 7077 8080 8081 18080

# Run as non-root spark user
USER 185

ENTRYPOINT ["/entrypoint.sh"]

