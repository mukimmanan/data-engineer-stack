# Use the official Apache Hive 4.1.0 image as the base
FROM apache/hive:4.0.1

# Define environment variables for the Metastore DB and MinIO configuration
# NOTE: The Metastore requires an external database (like Postgres/MySQL) to store metadata.
# These environment variables configure the Metastore database connection.
ENV DB_DRIVER=postgres
ENV DB_NAME=hive
ENV DB_HOST=postgres
ENV DB_USER=hive
ENV DB_PASS=hive
ENV METASTORE_PORT=9083

# --- MinIO/S3A Configuration ---

# The official Hive image includes the necessary Hadoop AWS Jars (like hadoop-aws.jar and aws-java-sdk-bundle.jar)
# in '/opt/hadoop/share/hadoop/tools/lib'. We need to move them to a location where Hive/Hadoop can find them
# to enable S3A/MinIO connectivity.

USER root

RUN apt-get update && apt-get install -y curl \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Move S3A Jars into the main Hadoop common lib directory
RUN set -ex \
    && ln -s /opt/hadoop/share/hadoop/tools/lib/hadoop-aws* /opt/hadoop/share/hadoop/common/lib/ \
    && ln -s /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk* /opt/hadoop/share/hadoop/common/lib/


ENV PG_DRIVER_VERSION=42.7.3
ENV PG_DRIVER_URL=https://jdbc.postgresql.org/download/postgresql-${PG_DRIVER_VERSION}.jar

RUN curl -o /opt/hive/lib/postgresql-${PG_DRIVER_VERSION}.jar ${PG_DRIVER_URL}

# Copy the configuration file template (hive-site.xml) into the custom conf directory.
# You will need to create a 'hive-site.xml' file in the same directory as this Dockerfile
# that contains the S3A and Metastore database configuration.

ARG AWS_SDK_BUNDLE_VERSION=1.12.794
# Download S3/Hadoop AWS libraries compatible with Spark 3.5.2 (Hadoop 3.3.x)
RUN curl -f -L -o /opt/hive/lib/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar
COPY hive-metastore/hive-site.xml /opt/hive/conf/hive-site.xml

ARG AWS_SDK_VERSION=2.39.5
ENV AWS_BUNDLE_JAR_URL=https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar

RUN curl -o /opt/hive/lib/aws-sdk-bundle-${AWS_SDK_VERSION}.jar ${AWS_BUNDLE_JAR_URL} \
    && echo "AWS SDK Bundle installed to /opt/hive/lib/"

ENV SCALA_VERSION="2.13"
ENV DELTA_STANDALONE_VERSION="0.6.0"
ENV PARQUET_HADOOP_VERSION="1.12.3"
ENV MAVEN_URL="https://repo1.maven.org/maven2"

RUN curl -f -L -o /opt/hive/lib/delta-standalone_${SCALA_VERSION}-${DELTA_STANDALONE_VERSION}.jar \
    ${MAVEN_URL}/io/delta/delta-standalone_${SCALA_VERSION}/${DELTA_STANDALONE_VERSION}/delta-standalone_${SCALA_VERSION}-${DELTA_STANDALONE_VERSION}.jar \
    && echo "Downloaded Delta Standalone."


# Switch back to the non-root user
USER hive

# Default command to run the Metastore service
CMD ["/opt/hive/bin/entrypoint.sh", "metastore"]