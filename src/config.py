import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WebSocket settings
    WEBSOCKET_HOST = os.getenv('WEBSOCKET_HOST', 'localhost')
    WEBSOCKET_PORT = os.getenv('WEBSOCKET_PORT', 5000)

    # Kafka configuration
    KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'chat_messages')

    # Other configurations can be added here