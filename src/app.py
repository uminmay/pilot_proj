from flask import Flask
from flask_socketio import SocketIO
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

# Import routes with correct paths
from .auth.routes import auth_bp
from .chat.routes import chat_bp

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    socketio.run(app, debug=True)