from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from src.db.models import ChatMessage
from src.kafka.producer import send_message_to_kafka

chat_bp = Blueprint('chat', __name__)
socketio = SocketIO()

@chat_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = ChatMessage.query.all()
    return jsonify([message.to_dict() for message in messages])

@chat_bp.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    new_message = ChatMessage(content=data['content'], user_id=data['user_id'])
    new_message.save()
    send_message_to_kafka(new_message.to_dict())
    socketio.emit('new_message', new_message.to_dict())
    return jsonify(new_message.to_dict()), 201

@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Connected to chat!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')