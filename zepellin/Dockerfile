# Use the latest stable Zeppelin image
FROM apache/zeppelin:0.12.0

USER root

# 1. System Updates & Python (Required for PySpark)
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Trino CLI (Enables the literal "!trino" shell command)
# We download the executable jar and make it executable as 'trino'
ARG TRINO_VERSION=478
RUN mkdir -p /opt/zeppelin/interpreter/trino
RUN wget -q https://repo1.maven.org/maven2/io/trino/trino-jdbc/${TRINO_VERSION}/trino-jdbc-${TRINO_VERSION}.jar -O /opt/zeppelin/interpreter/trino/trino-jdbc-${TRINO_VERSION}.jar && \
    chmod +x /opt/zeppelin/interpreter/trino/trino-jdbc-${TRINO_VERSION}.jar

# 3. (Optional) Install Python libraries commonly used with PySpark
RUN pip3 install pandas numpy matplotlib trino

# 4. Install Spark 4.0.1
COPY spark_install.sh /tmp/spark_install.sh
RUN chmod +x /tmp/spark_install.sh && /tmp/spark_install.sh

RUN apt-get update && apt-get install -y openjdk-17-jre-headless && \
    apt-get clean

# Set JAVA_HOME to the new Java 17 installation path
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Ensure Java 17 is used by default
ENV PATH=$JAVA_HOME/bin:$PATH

# Revert to the default zeppelin user
USER 1000