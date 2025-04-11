from kafka import KafkaConsumer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka consumer configuration
KAFKA_TOPIC = 'your_topic_name'  # Replace with your Kafka topic
KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address

def consume_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='your_group_id'  # Replace with your consumer group ID
    )

    try:
        for message in consumer:
            logger.info(f"Received message: {message.value}")
            # Process the message here
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()