#!/bin/bash

# --- Maven Dependency Downloader Script ---
# This script parses a list of dependencies (in the format groupId#artifactId;version)
# and downloads the corresponding JAR files from Maven Central.

# Configuration
MAVEN_URL="https://repo1.maven.org/maven2"
DOWNLOAD_DIR="/opt/spark/hive-spark-jars"

# Input list of dependencies (Parsed from your prompt, ignoring the "from central in [default]" part)
# NOTE: This list only includes the artifacts *not* marked as 'evicted modules'.
DEPENDENCIES=$(cat <<EOF
aopalliance#aopalliance;1.0
asm#asm;3.3.1
cglib#cglib;2.2.2
ch.qos.reload4j#reload4j;1.2.22
com.amazonaws.secretsmanager#aws-secretsmanager-caching-java;1.0.1
com.carrotsearch#hppc;0.7.2
com.cedarsoftware#java-util;1.9.0
com.cedarsoftware#json-io;2.5.1
com.esri.geometry#esri-geometry-api;2.2.4
com.fasterxml.jackson.core#jackson-annotations;2.16.1
com.fasterxml.jackson.core#jackson-core;2.16.1
com.fasterxml.jackson.core#jackson-databind;2.16.1
com.fasterxml.jackson.datatype#jackson-datatype-jsr310;2.16.1
com.fasterxml.jackson.jaxrs#jackson-jaxrs-base;2.16.1
com.fasterxml.jackson.jaxrs#jackson-jaxrs-json-provider;2.16.1
com.fasterxml.jackson.module#jackson-module-jaxb-annotations;2.16.1
com.fasterxml.woodstox#woodstox-core;5.4.0
com.github.ben-manes.caffeine#caffeine;2.8.4
com.github.joshelser#dropwizard-metrics-hadoop-metrics2-reporter;0.1.2
com.github.pjfanning#jersey-json;1.20
com.github.stephenc.jcip#jcip-annotations;1.0-1
com.google.android#annotations;4.1.1.4
com.google.api.grpc#proto-google-common-protos;2.9.0
com.google.code.findbugs#jsr305;3.0.2
com.google.code.gson#gson;2.9.0
com.google.errorprone#error_prone_annotations;2.14.0
com.google.flatbuffers#flatbuffers-java;1.12.0
com.google.guava#guava;22.0
com.google.inject#guice;4.0
com.google.inject.extensions#guice-servlet;4.0
com.google.j2objc#j2objc-annotations;1.1
com.google.protobuf#protobuf-java;3.24.4
com.google.re2j#re2j;1.2
com.jayway.jsonpath#json-path;2.9.0
com.jcraft#jsch;0.1.55
com.microsoft.sqlserver#mssql-jdbc;6.2.1.jre8
com.nimbusds#nimbus-jose-jwt;9.8.1
com.squareup.okhttp3#okhttp;4.9.3
com.squareup.okio#okio;2.8.0
com.sun.jersey#jersey-client;1.19.4
com.sun.jersey#jersey-core;1.19.4
com.sun.jersey#jersey-server;1.19.4
com.sun.jersey#jersey-servlet;1.19.4
com.sun.jersey.contribs#jersey-guice;1.19.4
com.sun.jersey.contribs#jersey-multipart;1.19.4
com.sun.xml.bind#jaxb-impl;2.2.3-1
com.tdunning#json;1.8
com.zaxxer#HikariCP;4.0.3
com.zaxxer#HikariCP-java7;2.4.12
commons-beanutils#commons-beanutils;1.9.2
commons-cli#commons-cli;1.5.0
commons-codec#commons-codec;1.15
commons-collections#commons-collections;3.2.2
commons-configuration#commons-configuration;1.10
commons-daemon#commons-daemon;1.0.13
commons-digester#commons-digester;1.8.1
commons-io#commons-io;2.12.0
commons-lang#commons-lang;2.6
commons-logging#commons-logging;1.2
commons-net#commons-net;3.9.0
commons-validator#commons-validator;1.6
de.ruedigermoeller#fst;2.50
dnsjava#dnsjava;2.1.7
io.airlift#aircompressor;0.21
io.dropwizard.metrics#metrics-core;3.1.0
io.dropwizard.metrics#metrics-json;3.1.0
io.dropwizard.metrics#metrics-jvm;3.1.0
io.grpc#grpc-api;1.51.0
io.grpc#grpc-context;1.51.0
io.grpc#grpc-core;1.51.0
io.grpc#grpc-netty-shaded;1.51.0
io.grpc#grpc-protobuf;1.51.0
io.grpc#grpc-protobuf-lite;1.51.0
io.grpc#grpc-stub;1.51.0
io.jsonwebtoken#jjwt-api;0.10.5
io.jsonwebtoken#jjwt-impl;0.10.5
io.jsonwebtoken#jjwt-jackson;0.10.5
io.netty#netty;3.10.6.Final
io.netty#netty-all;4.1.89.Final
io.netty#netty-buffer;4.1.94.Final
io.netty#netty-codec;4.1.94.Final
io.netty#netty-codec-dns;4.1.89.Final
io.netty#netty-codec-haproxy;4.1.89.Final
io.netty#netty-codec-http;4.1.89.Final
io.netty#netty-codec-http2;4.1.89.Final
io.netty#netty-codec-memcache;4.1.89.Final
io.netty#netty-codec-mqtt;4.1.89.Final
io.netty#netty-codec-redis;4.1.89.Final
io.netty#netty-codec-smtp;4.1.89.Final
io.netty#netty-codec-socks;4.1.89.Final
io.netty#netty-codec-stomp;4.1.89.Final
io.netty#netty-codec-xml;4.1.89.Final
io.netty#netty-common;4.1.94.Final
io.netty#netty-handler;4.1.94.Final
io.netty#netty-handler-proxy;4.1.89.Final
io.netty#netty-handler-ssl-ocsp;4.1.89.Final
io.netty#netty-resolver;4.1.94.Final
io.netty#netty-resolver-dns;4.1.89.Final
io.netty#netty-resolver-dns-classes-macos;4.1.89.Final
io.netty#netty-resolver-dns-native-macos;4.1.89.Final
io.netty#netty-transport;4.1.94.Final
io.netty#netty-transport-classes-epoll;4.1.94.Final
io.netty#netty-transport-classes-kqueue;4.1.89.Final
io.netty#netty-transport-native-epoll;4.1.94.Final
io.netty#netty-transport-native-kqueue;4.1.89.Final
io.netty#netty-transport-native-unix-common;4.1.94.Final
io.netty#netty-transport-rxtx;4.1.89.Final
io.netty#netty-transport-sctp;4.1.89.Final
io.netty#netty-transport-udt;4.1.89.Final
io.perfmark#perfmark-api;0.25.0
jakarta.activation#jakarta.activation-api;1.2.1
jakarta.xml.bind#jakarta.xml.bind-api;2.3.3
javax.annotation#javax.annotation-api;1.3.2
javax.inject#javax.inject;1
javax.servlet#javax.servlet-api;3.1.0
javax.servlet.jsp#jsp-api;2.1
javax.transaction#javax.transaction-api;1.3
javax.ws.rs#jsr311-api;1.1.1
javax.xml.bind#jaxb-api;2.2.11
javolution#javolution;5.5.1
jline#jline;2.14.6
joda-time#joda-time;2.9.9
net.minidev#accessors-smart;2.5.0
net.minidev#json-smart;2.5.0
net.sf.jpam#jpam;1.1
net.sf.opencsv#opencsv;2.3
org.antlr#ST4;4.0.4
org.antlr#antlr-runtime;3.5.2
org.antlr#antlr4-runtime;4.9.3
org.apache.ant#ant;1.10.13
org.apache.ant#ant-launcher;1.10.13
org.apache.arrow#arrow-format;12.0.0
org.apache.arrow#arrow-memory-core;12.0.0
org.apache.arrow#arrow-memory-netty;12.0.0
org.apache.arrow#arrow-vector;12.0.0
org.apache.atlas#atlas-client-common;2.3.0
org.apache.atlas#atlas-client-v2;2.3.0
org.apache.atlas#atlas-intg;2.3.0
org.apache.avro#avro;1.11.3
org.apache.commons#commons-collections4;4.1
org.apache.commons#commons-compress;1.23.0
org.apache.commons#commons-configuration2;2.8.0
org.apache.commons#commons-dbcp2;2.9.0
org.apache.commons#commons-jexl3;3.3
org.apache.commons#commons-lang3;3.12.0
org.apache.commons#commons-math3;3.6.1
org.apache.commons#commons-pool2;2.11.1
org.apache.commons#commons-text;1.10.0
org.apache.derby#derby;10.14.2.0
org.apache.geronimo.specs#geronimo-jcache_1.0_spec;1.0-alpha-1
org.apache.hadoop#hadoop-annotations;3.4.1
org.apache.hadoop#hadoop-auth;3.4.1
org.apache.hadoop#hadoop-client-api;3.4.1
org.apache.hadoop#hadoop-client-runtime;3.4.1
org.apache.hadoop#hadoop-common;3.4.1
org.apache.hadoop#hadoop-hdfs;3.4.1
org.apache.hadoop#hadoop-hdfs-client;3.4.1
org.apache.hadoop#hadoop-registry;3.4.1
org.apache.hadoop#hadoop-yarn-api;3.4.1
org.apache.hadoop#hadoop-yarn-client;3.4.1
org.apache.hadoop#hadoop-yarn-common;3.4.1
org.apache.hadoop#hadoop-yarn-registry;3.4.1
org.apache.hadoop#hadoop-yarn-server-applicationhistoryservice;3.4.1
org.apache.hadoop#hadoop-yarn-server-common;3.4.1
org.apache.hadoop#hadoop-yarn-server-resourcemanager;3.4.1
org.apache.hadoop#hadoop-yarn-server-web-proxy;3.4.1
org.apache.hadoop.thirdparty#hadoop-shaded-guava;1.1.1
org.apache.hadoop.thirdparty#hadoop-shaded-protobuf_3_7;1.1.1
org.apache.hive#hive-classification;4.0.1
org.apache.hive#hive-common;4.0.1
org.apache.hive#hive-exec;4.0.1
org.apache.hive#hive-llap-client;4.0.1
org.apache.hive#hive-llap-common;4.0.1
org.apache.hive#hive-llap-tez;4.0.1
org.apache.hive#hive-metastore;4.0.1
org.apache.hive#hive-serde;4.0.1
org.apache.hive#hive-service-rpc;4.0.1
org.apache.hive#hive-shims;4.0.1
org.apache.hive#hive-standalone-metastore-common;4.0.1
org.apache.hive#hive-storage-api;4.0.1
org.apache.hive.shims#hive-shims-0.23;4.0.1
org.apache.hive.shims#hive-shims-common;4.0.1
org.apache.httpcomponents#httpclient;4.5.13
org.apache.httpcomponents#httpcore;4.4.13
org.apache.ivy#ivy;2.5.2
org.apache.kerby#kerb-admin;1.0.1
org.apache.kerby#kerb-client;1.0.1
org.apache.kerby#kerb-common;1.0.1
org.apache.kerby#kerb-core;1.0.1
org.apache.kerby#kerb-crypto;1.0.1
org.apache.kerby#kerb-identity;1.0.1
org.apache.kerby#kerb-server;1.0.1
org.apache.kerby#kerb-simplekdc;1.0.1
org.apache.kerby#kerb-util;1.0.1
org.apache.kerby#kerby-asn1;1.0.1
org.apache.kerby#kerby-config;1.0.1
org.apache.kerby#kerby-pkix;1.0.1
org.apache.kerby#kerby-util;1.0.1
org.apache.kerby#kerby-xdr;1.0.1
org.apache.kerby#token-provider;1.0.1
org.apache.logging.log4j#log4j-1.2-api;2.18.0
org.apache.logging.log4j#log4j-core;2.18.0
org.apache.logging.log4j#log4j-slf4j-impl;2.18.0
org.apache.logging.log4j#log4j-web;2.18.0
org.apache.orc#orc-core;1.8.5
org.apache.orc#orc-shims;1.8.5
org.apache.parquet#parquet-hadoop-bundle;1.13.1
org.apache.tez#tez-api;0.10.4
org.apache.thrift#libfb303;0.9.3
org.apache.thrift#libthrift;0.16.0
org.apache.yetus#audience-annotations;0.12.0
org.apache.zookeeper#zookeeper;3.8.3
org.apache.zookeeper#zookeeper-jute;3.8.3
org.bouncycastle#bcpkix-jdk15on;1.68
org.bouncycastle#bcprov-jdk15on;1.68
org.checkerframework#checker-qual;3.4.0
org.codehaus.groovy#groovy-all;2.4.21
org.codehaus.janino#commons-compiler;3.0.11
org.codehaus.janino#janino;3.0.11
org.codehaus.jettison#jettison;1.5.4
org.codehaus.mojo#animal-sniffer-annotations;1.21
org.codehaus.woodstox#stax2-api;4.2.1
org.datanucleus#datanucleus-api-jdo;5.2.8
org.datanucleus#datanucleus-core;5.2.10
org.datanucleus#datanucleus-rdbms;5.2.10
org.datanucleus#javax.jdo;3.2.0-release
org.eclipse.jetty#jetty-client;9.4.51.v20230217
org.eclipse.jetty#jetty-http;9.4.51.v20230217
org.eclipse.jetty#jetty-io;9.4.51.v20230217
org.eclipse.jetty#jetty-rewrite;9.4.45.v20220203
org.eclipse.jetty#jetty-security;9.4.45.v20220203
org.eclipse.jetty#jetty-server;9.4.51.v20230217
org.eclipse.jetty#jetty-servlet;9.4.45.v20220203
org.eclipse.jetty#jetty-util;9.4.51.v20230217
org.eclipse.jetty#jetty-util-ajax;9.4.51.v20230217
org.eclipse.jetty#jetty-webapp;9.4.45.v20220203
org.eclipse.jetty#jetty-xml;9.4.45.v20220203
org.eclipse.jetty.websocket#websocket-api;9.4.51.v20230217
org.eclipse.jetty.websocket#websocket-client;9.4.51.v20230217
org.eclipse.jetty.websocket#websocket-common;9.4.51.v20230217
org.ehcache#ehcache;3.3.1
org.fusesource.jansi#jansi;2.4.0
org.fusesource.leveldbjni#leveldbjni-all;1.8
org.glassfish.corba#glassfish-corba-omgapi;4.2.2
org.javassist#javassist;3.28.0-GA
org.jetbrains#annotations;17.0.0
org.jetbrains.kotlin#kotlin-stdlib;1.4.10
org.jetbrains.kotlin#kotlin-stdlib-common;1.4.10
org.jline#jline;3.9.0
org.jvnet.mimepull#mimepull;1.9.3
org.objenesis#objenesis;2.6
org.ow2.asm#asm;9.3
org.reflections#reflections;0.10.2
org.slf4j#slf4j-api;1.7.36
org.springframework#spring-aop;5.3.21
org.springframework#spring-beans;5.3.21
org.springframework#spring-context;5.3.21
org.springframework#spring-core;5.3.21
org.springframework#spring-expression;5.3.21
org.springframework#spring-jcl;5.3.21
org.springframework#spring-jdbc;5.3.21
org.springframework#spring-tx;5.3.21
org.threeten#threeten-extra;1.7.1
org.xerial.snappy#snappy-java;1.1.10.4
stax#stax-api;1.0.1
EOF
)

echo "--- Starting dependency download from Maven Central ---"
echo "Target directory: $DOWNLOAD_DIR"

# Create the target directory
mkdir -p "$DOWNLOAD_DIR"

# Loop through each dependency line
echo "$DEPENDENCIES" | while IFS= read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue

    # 1. Parse GroupId, ArtifactId, Version from groupId#artifactId;version
    GROUP_ID_PART=$(echo "$line" | cut -d '#' -f 1)
    ARTIFACT_ID=$(echo "$line" | cut -d '#' -f 2 | cut -d ';' -f 1)
    VERSION=$(echo "$line" | cut -d ';' -f 2)

    # Sanity check for parsing
    if [[ -z "$GROUP_ID_PART" || -z "$ARTIFACT_ID" || -z "$VERSION" ]]; then
        echo "Warning: Could not parse line: $line. Skipping."
        continue
    fi

    # 2. Transform GroupId (dots to slashes)
    GROUP_PATH=$(echo "$GROUP_ID_PART" | tr '.' '/')

    # 3. Construct the full Maven URL path
    # Example: https://repo1.maven.org/maven2/com/google/guava/guava/22.0/guava-22.0.jar
    DOWNLOAD_URL="${MAVEN_URL}/${GROUP_PATH}/${ARTIFACT_ID}/${VERSION}/${ARTIFACT_ID}-${VERSION}.jar"
    OUTPUT_FILE="${DOWNLOAD_DIR}/${ARTIFACT_ID}-${VERSION}.jar"

    echo "Downloading: $ARTIFACT_ID-$VERSION.jar"

    # 4. Download the file using curl, with retry logic and silent output
    # -L: Follow redirects
    # -s: Silent mode
    # -f: Fail fast on HTTP errors (404)
    # -o: Output filename
    if ! curl -Lsf --retry 3 -o "$OUTPUT_FILE" "$DOWNLOAD_URL"; then
        echo "--- ERROR: Failed to download $DOWNLOAD_URL ---"
        echo "Check if the GAV coordinates or the JAR filename structure is correct for this artifact."
    fi
done

echo "--- Download process complete. Check the '$DOWNLOAD_DIR' folder. ---"
