from kafka import KafkaConsumer

# Consumer 1
consumer1 = KafkaConsumer(
    'another-topic-jan-task',
    bootstrap_servers='172.18.0.2:9092',
    group_id='consumer-group-1',
    auto_offset_reset='earliest',
)
for message in consumer1:
    print(f"Consumer 1 received: {message.value.decode('utf-8')}")
consumer1.close()
