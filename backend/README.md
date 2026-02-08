# Todo Backend API

This is the backend component for the Todo Full-Stack Web Application, built with FastAPI and SQLModel.

## Features

- RESTful API for task management
- Multi-user support with user isolation
- JWT-based authentication
- SQLite/PostgreSQL database support
- Complete CRUD operations for tasks

## API Endpoints

- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Running Tests

```bash
pytest tests/
```

## Architecture

The backend follows a layered architecture:
- **API Layer**: FastAPI endpoints
- **Service Layer**: Business logic
- **Model Layer**: Data models and database interactions
- **Database Layer**: SQLModel with PostgreSQL/SQLite