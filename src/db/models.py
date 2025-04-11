from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)

    sessions = relationship("Session", back_populates="user")

    def __init__(self, username, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.hashed_password = password  # In production, use proper hashing

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_token = Column(String, unique=True)

    user = relationship("User", back_populates="sessions")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)

    sender = relationship("User")