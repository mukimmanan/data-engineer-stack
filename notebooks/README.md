# Notebooks

This directory organizes interactive analysis and streaming pipelines structured into **folders per DAG**.

## Directory Structure

```text
notebooks/
└── daily_kafka_to_delta_spark_job/
    └── stream_kafka_to_delta_2KAFKADLT.zpln  # Apache Zeppelin Notebook (.zpln)
```

## Format: Apache Zeppelin (`.zpln`)
Notebooks are formatted as Apache Zeppelin notes (`.zpln`):
* Interactive multi-language paragraphs: `%spark.pyspark`, `%spark.sql`, `%md`
* Natively synced with the Spark cluster Zeppelin workspace (`spark/zep_notebooks/`)
* Hierarchical tree view: naming convention `DAG_ID/note_name` automatically groups notebooks in Zeppelin's UI.
