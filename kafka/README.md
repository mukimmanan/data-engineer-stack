# Kafka & CDC Event Streaming
This directory manages real-time event streaming and Change Data Capture (CDC).

## Components
* **Apache Kafka (KRaft)**: A 3-node cluster (v4.2.2) running in combined KRaft mode (no ZooKeeper required).
* **Debezium Connect**: Kafka Connect worker (v3.0) pre-loaded with Debezium plugins for extracting CDC logs.
* **Schema Registry**: Confluent Schema Registry (v7.7.0) for managing Avro/Protobuf schemas.
* **Conduktor Console**: A modern UI (accessible at port 8088) to visually manage Kafka topics, connectors, and schemas.

## CDC Workflow
Debezium Connect listens to logical replication logs from the postgres container and streams row-level changes (Inserts, Updates, Deletes) as real-time events into Kafka topics.
