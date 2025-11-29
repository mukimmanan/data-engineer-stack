FROM apache/spark:3.5.2

USER root

# Allow overriding aws/hadoop aws versions at build time
ARG HADOOP_AWS_VERSION=3.3.4
ARG AWS_SDK_BUNDLE_VERSION=1.12.548

# Download S3/Hadoop AWS libraries compatible with Spark 3.5.2 (Hadoop 3.3.x)
RUN mkdir -p /opt/spark/jars && \
    curl -f -L -o /opt/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl -f -L -o /opt/spark/jars/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar && \
    curl -f -L -o /opt/spark/jars/httpclient-4.5.14.jar https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.14/httpclient-4.5.14.jar && \
    curl -f -L -o /opt/spark/jars/delta-spark_2.12-3.3.2.jar https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.3.2/delta-spark_2.12-3.3.2.jar && \
    curl -f -L -o /opt/spark/jars/iceberg-spark-runtime-3.5_2.12:1.10.0.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.13/1.10.0/iceberg-spark-runtime-3.5_2.13-1.10.0.jar
    
# Create eventlog directory
RUN mkdir -p /eventlog && chmod 777 /eventlog

# Copy Spark configuration
COPY conf/ /opt/spark/conf/

# Entrypoint script to select role
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
