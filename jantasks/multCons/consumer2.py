from kafka import KafkaConsumer

# Consumer 2
consumer2 = KafkaConsumer(
    'another-topic-jan-task',
    bootstrap_servers='172.18.0.2:9092',
    group_id='consumer-group-1',
    auto_offset_reset='earliest'
)

for message in consumer2:
    print(f"Consumer 2 received: {message.value.decode('utf-8')}")
    
consumer2.close()    