from confluent_kafka.admin import AdminClient, NewTopic
BROKER = "172.18.0.2:9092" 
admin_client = AdminClient({
    "bootstrap.servers": BROKER
})
TOPIC_NAME = "another-topic-jan-task"
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1  

def create_topic(topic_name, num_partitions, replication_factor):
    topic = NewTopic(
        topic=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    try:
        futures = admin_client.create_topics([topic])
        for topic, future in futures.items():
            try:
                future.result()  
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    except Exception as e:
        print(f"Error while creating topic: {e}")
create_topic(TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR)
    