from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from .db import db  # Import SQLAlchemy instance

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)  # Initialize SQLAlchemy
socketio = SocketIO(app)

# Import routes with correct paths
from .auth.routes import auth_bp
from .chat.routes import chat_bp

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    socketio.run(app, debug=True)