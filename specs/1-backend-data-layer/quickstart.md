# Quickstart Guide: Core Backend & Data Layer for Todo Full-Stack Web Application

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Neon PostgreSQL connection details
   ```

6. **Initialize the database**:
   ```bash
   # The application will auto-create tables on first run
   python -c "from src.database.database import engine, SQLModel; SQLModel.metadata.create_all(engine)"
   ```

7. **Run the application**:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Endpoints

Once running, the API will be available at `http://localhost:8000`:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task by ID
- `PUT /api/{user_id}/tasks/{id}` - Update an existing task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task

## Example Usage

### Create a Task
```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "This is a sample task"}'
```

### Get All Tasks for a User
```bash
curl http://localhost:8000/api/user123/tasks
```

### Get a Specific Task
```bash
curl http://localhost:8000/api/user123/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/user123/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task Title", "completed": true}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/user123/tasks/1
```

## Running Tests

```bash
pytest tests/
```

## Environment Variables

- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token signing (if authentication is implemented)