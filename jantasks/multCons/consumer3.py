from kafka import KafkaConsumer

# Consumer 2
consumer3 = KafkaConsumer(
    'another-topic-jan-task',
    bootstrap_servers='172.18.0.2:9092',
    group_id='consumer-group-1',
    auto_offset_reset='earliest'
)

for message in consumer3:
    print(f"Consumer 3 received: {message.value.decode('utf-8')}")
    
consumer3.close()    