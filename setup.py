from setuptools import setup, find_packages

setup(
    name="chat-app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-JWT-Extended',
        'Flask-SocketIO',
        'channels',
    ],
)
