from confluent_kafka import Producer
import time

BROKER = "172.18.0.2:9092"  
TOPIC = "another-topic-jan-task"  
producer_config = {
    "bootstrap.servers": BROKER
}
producer = Producer(producer_config)

for value in range(100, 200): 
    time.sleep(2)
    producer.produce(
        TOPIC,
        value=str(value),  
    )
    producer.flush()  

print("Finished producing messages from 1 to 500.")
