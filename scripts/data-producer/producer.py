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
from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

TOPIC_NAME = "global_financial_transactions"
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 3
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092,localhost:9094,localhost:9096")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")

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

def ensure_topic_partitions(bootstrap_servers, topic_name, num_partitions=3, replication_factor=3):
    """Ensures that the topic exists with at least num_partitions partitions."""
    print(f"Checking partitions for topic '{topic_name}'...")
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
    try:
        metadata = admin_client.list_topics(timeout=10)
        num_brokers = len(metadata.brokers)
        effective_rf = min(replication_factor, num_brokers) if num_brokers > 0 else 1

        if topic_name not in metadata.topics:
            print(f"Topic '{topic_name}' does not exist. Creating with {num_partitions} partitions (RF: {effective_rf})...")
            new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=effective_rf)
            futures = admin_client.create_topics([new_topic])
            for t, f in futures.items():
                try:
                    f.result()
                    print(f"Topic '{t}' successfully created with {num_partitions} partitions.")
                except Exception as e:
                    print(f"Notice during topic creation: {e}")
        else:
            topic_metadata = metadata.topics[topic_name]
            current_partitions = len(topic_metadata.partitions)
            print(f"Topic '{topic_name}' currently has {current_partitions} partition(s).")
            if current_partitions < num_partitions:
                print(f"Altering topic '{topic_name}' to expand to {num_partitions} partitions...")
                futures = admin_client.create_partitions([NewPartitions(topic_name, num_partitions)])
                for t, f in futures.items():
                    try:
                        f.result()
                        print(f"Topic '{t}' successfully updated to {num_partitions} partitions.")
                    except Exception as e:
                        print(f"Notice during partition expansion: {e}")
            else:
                print(f"Topic '{topic_name}' already configured with {current_partitions} partitions.")
    except Exception as e:
        print(f"Warning: AdminClient check skipped or failed ({e}). Proceeding to produce...")

def main():
    print(f"Connecting to Kafka Brokers at {BOOTSTRAP_SERVERS}...")
    ensure_topic_partitions(BOOTSTRAP_SERVERS, TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR)

    print(f"Setting up Schema Registry Client at {SCHEMA_REGISTRY_URL}...")
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    print("Configuring Protobuf Serializer...")
    protobuf_serializer = ProtobufSerializer(
        transaction_pb2.Transaction,
        schema_registry_client,
        conf={'use.deprecated.format': False}
    )

    producer_conf = {'bootstrap.servers': BOOTSTRAP_SERVERS}
    producer = Producer(producer_conf)
    
    string_serializer = StringSerializer('utf_8')

    print(f"Starting stream to topic '{TOPIC_NAME}' (3 Partitions)... Press Ctrl+C to stop.")
    
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

