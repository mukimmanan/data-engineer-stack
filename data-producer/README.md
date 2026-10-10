# Kafka Protobuf Data Producer

This directory contains a Python streaming application that generates rich, fake financial transaction data and pushes it into Kafka using Protobuf serialization and Confluent Schema Registry.

## Dataset Details
- **Topic Name**: `global_financial_transactions`
- **Format**: Protocol Buffers (`transaction.proto`)
- **Fields Generated**: Transaction ID, amounts, currency, fraud flags, device types, along with nested objects for User data (name, IP, email) and Location data (latitude, longitude, city, country).

## Setup Instructions

1. Ensure your Kafka and Schema Registry cluster is running:
   ```bash
   cd ..
   .\stack.ps1 up
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   cd data-producer
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the producer! (The script will automatically compile the Protobuf schema for you)
   ```bash
   python producer.py
   ```
