from kafka import KafkaProducer
import json
import os

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()

    def close(self):
        self.producer.close()

def send_message_to_kafka(message):
    producer = Producer()
    try:
        producer.send_message('chat_messages', message)
    finally:
        producer.close()