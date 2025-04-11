from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = SQLAlchemy()
Base = declarative_base()
engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
db_session = Session()