# README.md

# Chat Application

This project is a real-time chat application built with Python. It supports user accounts, session management using PostgreSQL, and real-time communication through WebSockets. The application is designed to handle multiple users and utilizes Kafka for message handling.

## Features

- User authentication and account management
- Real-time chat functionality
- Session management with PostgreSQL
- Scalable architecture using Kafka
- Comprehensive unit tests for all functionalities

## Project Structure

```
chat-app
├── src
│   ├── auth                # User authentication module
│   ├── chat                # Real-time chat module
│   ├── db                  # Database models and interactions
│   ├── kafka               # Kafka message handling
│   ├── tests               # Unit tests
│   ├── app.py              # Main entry point of the application
│   └── config.py           # Configuration settings
├── docker-compose.yml       # Docker services configuration
├── Dockerfile               # Docker image build instructions
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:uminmay/pilot_proj.git
   cd pilot_proj
   ```

2. Set up a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r src/requirements.txt
   ```

4. Set up your PostgreSQL database and update the `.env` file with your database credentials.

5. Run the application:
   ```
   python src/app.py
   ```

## Testing

To run the tests, use the following command:
```
pytest src/tests
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.