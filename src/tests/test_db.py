import pytest
from ...src.db.models import User, Session  # Fix import path
from ...src.db import db_session, Base, engine  # Fix import path

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def new_user():
    user = User(username='testuser', password='testpass')
    db_session.add(user)
    db_session.commit()
    yield user
    db_session.delete(user)
    db_session.commit()

def test_user_creation(new_user):
    assert new_user.username == 'testuser'
    assert new_user.password == 'testpass'

def test_session_creation(new_user):
    session = Session(user_id=new_user.id)
    db_session.add(session)
    db_session.commit()
    assert session.user_id == new_user.id
    db_session.delete(session)
    db_session.commit()