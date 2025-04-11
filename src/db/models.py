from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db  # Import SQLAlchemy instance instead of Base

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, index=True)
    hashed_password = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True, nullable=True)

    sessions = db.relationship("Session", back_populates="user")

    def __init__(self, username, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.hashed_password = password  # In production, use proper hashing

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    session_token = db.Column(db.String, unique=True)

    user = db.relationship("User", back_populates="sessions")

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True, index=True)
    sender_id = db.Column(db.Integer, ForeignKey('users.id'))
    content = db.Column(db.String)

    sender = db.relationship("User")