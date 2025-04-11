# File: /chat-app/chat-app/src/db/__init__.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
db_session = Session()