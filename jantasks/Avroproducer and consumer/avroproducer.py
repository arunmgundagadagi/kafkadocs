from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
# defining avro schema for the serializibng
value_schema_str = """                      
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"}
  ]
}
"""

# Set up the Avro schema
value_schema = avro.loads(value_schema_str)

# Kafka and Schema Registry configuration
config = {
    'bootstrap.servers': 'localhost:9092',   # Kafka broker
    'schema.registry.url': 'http://localhost:8081'  # Schema Registry
}

# Create the AvroProducer
producer = AvroProducer(config, default_value_schema=value_schema)

# Produce messages
try:
    for i in range(10):
        value = {"name": f"User_{i+30}", "age": 20 + i + 30}  # Message content
        producer.produce(topic='avro-topic', value=value)
        producer.flush()  # Ensure all messages are sent
        print(f"Produced message: {value}")

except Exception as e:
    print(f"Failed to produce message: {e}")