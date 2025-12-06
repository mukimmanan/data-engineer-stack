FROM apache/spark:4.0.1

USER root

# Allow overriding aws/hadoop aws versions at build time
ARG HADOOP_AWS_VERSION=3.4.1
ARG AWS_SDK_BUNDLE_VERSION=1.12.794

# Download S3/Hadoop AWS libraries compatible with Spark 4.0.1 (Hadoop 4.0.x)
RUN mkdir -p /opt/spark/jars && \
    curl -f -L -o /opt/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl -f -L -o /opt/spark/jars/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar && \
    curl -f -L -o /opt/spark/jars/httpclient-4.5.14.jar https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.14/httpclient-4.5.14.jar && \
    curl -f -L -o /opt/spark/jars/delta-spark_2.13-4.0.0.jar https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/4.0.0/delta-spark_2.13-4.0.0.jar && \
    curl -f -L -o /opt/spark/jars/iceberg-spark-runtime-4.0_2.13-1.10.0.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.0_2.13/1.10.0/iceberg-spark-runtime-4.0_2.13-1.10.0.jar
    
RUN curl -f -L -o /opt/spark/jars/delta-storage-4.0.0.jar https://repo1.maven.org/maven2/io/delta/delta-storage/4.0.0/delta-storage-4.0.0.jar

ARG AWS_SDK_VERSION=2.39.5
ENV AWS_BUNDLE_JAR_URL=https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar

RUN curl -f -L -o /opt/spark/jars/aws-sdk-bundle-${AWS_SDK_VERSION}.jar ${AWS_BUNDLE_JAR_URL} \
    && echo "AWS SDK Bundle installed"

RUN apt-get update && apt-get install -y unzip

# Copy Spark configuration
COPY conf/ /opt/spark/conf/
COPY ./hive_jars_401.sh /hive_jars.sh

RUN chmod +x /hive_jars.sh && /hive_jars.sh

# Entrypoint script to select role
ARG ZEPPELIN_VERSION=0.12.0
ENV ZEPPELIN_HOME=/opt/zeppelin
ENV ZEPPELIN_PACKAGE=zeppelin-${ZEPPELIN_VERSION}-bin-all
ENV ZEPPELIN_DOWNLOAD_URL=https://dlcdn.apache.org/zeppelin/zeppelin-${ZEPPELIN_VERSION}/${ZEPPELIN_PACKAGE}.tgz

RUN apt-get update && \
    apt-get install -y wget net-tools && \
    rm -rf /var/lib/apt/lists/*

# Install Zeppelin
RUN curl -f -L -o /tmp/zeppelin.tgz ${ZEPPELIN_DOWNLOAD_URL} && \
    mkdir -p ${ZEPPELIN_HOME} && \
    tar -xf /tmp/zeppelin.tgz -C /opt/ && \
    mv /opt/${ZEPPELIN_PACKAGE} ${ZEPPELIN_HOME} && \
    rm /tmp/zeppelin.tgz

RUN mv ${ZEPPELIN_HOME}/${ZEPPELIN_PACKAGE}/* ${ZEPPELIN_HOME}/ && \
    rm -rf ${ZEPPELIN_HOME}/${ZEPPELIN_PACKAGE}
# Set Spark as the default interpreter  
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PATH=$PATH:$SPARK_HOME/bin:$ZEPPELIN_HOME/bin
ENV JAVA_HOME=/opt/java/openjdk

RUN mkdir -p ${ZEPPELIN_HOME}/logs ${ZEPPELIN_HOME}/run ${ZEPPELIN_HOME}/notebook

RUN apt-get update && \
    apt-get install -y procps && \
    rm -rf /var/lib/apt/lists/*

ENV ZEPPELIN_JMX_ENABLE=false
ENV ZEPPELIN_JAVA_OPTS="--add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"

# --- Permissions ---
# Give ownership to the 'spark' user (UID 185)
RUN chown -R 185:0 ${ZEPPELIN_HOME} && \
    chmod -R g+w ${ZEPPELIN_HOME}

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
