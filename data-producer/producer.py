import os
import sys
import time
import random
from uuid import uuid4
from faker import Faker
import grpc_tools.protoc as protoc

# 1. Compile the Protobuf file dynamically
proto_file = "transaction.proto"
print(f"Compiling {proto_file}...")
protoc_args = [
    "grpc_tools.protoc",
    "--proto_path=.",
    "--python_out=.",
    proto_file
]
if protoc.main(protoc_args) != 0:
    print("Failed to compile protobuf!")
    sys.exit(1)

# Now we can import the generated Python class
import transaction_pb2
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

TOPIC_NAME = "global_financial_transactions"
BOOTSTRAP_SERVERS = "localhost:9092,localhost:9094,localhost:9096"
SCHEMA_REGISTRY_URL = "http://localhost:8081"

fake = Faker()

def generate_transaction():
    """Generates a rich, fake transaction record."""
    txn = transaction_pb2.Transaction()
    txn.transaction_id = str(uuid4())
    txn.timestamp = int(time.time() * 1000)
    txn.amount = round(random.uniform(5.0, 5000.0), 2)
    txn.currency = fake.currency_code()
    txn.merchant = fake.company()
    txn.transaction_type = random.choice(["PURCHASE", "REFUND", "TRANSFER", "WITHDRAWAL"])
    txn.is_flagged_fraud = random.random() < 0.02 # 2% chance of fraud
    txn.device_type = random.choice(["MOBILE", "DESKTOP", "TABLET", "POS_TERMINAL"])
    
    txn.user.user_id = str(fake.random_int(min=10000, max=99999))
    txn.user.full_name = fake.name()
    txn.user.email = fake.email()
    txn.user.ip_address = fake.ipv4()
    
    txn.location.country = fake.country()
    txn.location.city = fake.city()
    txn.location.latitude = float(fake.latitude())
    txn.location.longitude = float(fake.longitude())
    
    return txn

def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} [Partition: {msg.partition()}] at offset {msg.offset()}")

def main():
    print(f"Setting up Schema Registry Client at {SCHEMA_REGISTRY_URL}...")
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    print("Configuring Protobuf Serializer...")
    protobuf_serializer = ProtobufSerializer(
        transaction_pb2.Transaction,
        schema_registry_client,
        conf={'use.deprecated.format': False}
    )

    print(f"Connecting to Kafka Brokers at {BOOTSTRAP_SERVERS}...")
    producer_conf = {'bootstrap.servers': BOOTSTRAP_SERVERS}
    producer = Producer(producer_conf)
    
    string_serializer = StringSerializer('utf_8')

    print(f"Starting stream to topic '{TOPIC_NAME}'... Press Ctrl+C to stop.")
    
    try:
        while True:
            # Generate fake data
            transaction = generate_transaction()
            
            # Use User ID as the Kafka partitioning key
            key = transaction.user.user_id
            
            # Produce the message
            producer.produce(
                topic=TOPIC_NAME,
                key=string_serializer(key),
                value=protobuf_serializer(transaction, SerializationContext(TOPIC_NAME, MessageField.VALUE)),
                on_delivery=delivery_report
            )
            
            # Serve delivery callback queue
            producer.poll(0.0)
            
            # Sleep to simulate streaming rate
            time.sleep(random.uniform(0.1, 1.0))
            
    except KeyboardInterrupt:
        print("\nStopping streaming...")
    finally:
        print("Flushing remaining messages...")
        producer.flush()

if __name__ == '__main__':
    main()
