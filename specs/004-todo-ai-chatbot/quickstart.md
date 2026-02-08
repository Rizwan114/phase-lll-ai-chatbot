# Quickstart: Phase III - Todo AI Chatbot

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-08

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon account) or local PostgreSQL
- OpenAI API key

## Backend Setup

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

New Phase III dependencies (added to requirements.txt):
- `openai-agents` — OpenAI Agents SDK
- `mcp[cli]` — MCP server SDK

### 2. Configure environment

```bash
cp .env.example .env
```

Required environment variables:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Start the backend

```bash
uvicorn backend.src.main:app --reload --port 8000
```

The server will:
- Create database tables on startup (including new Conversation, Message)
- Serve the chat API at `POST /api/{user_id}/chat`
- Serve existing REST endpoints for backward compatibility

### 4. Test the chat API

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "Add a task to buy groceries"}'
```

Expected response:
```json
{
  "conversation_id": "uuid-here",
  "response": "I've added a new task: 'buy groceries'. Is there anything else you'd like to do?",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": {"title": "buy groceries"},
      "output": {"id": 1, "title": "buy groceries", "completed": false}
    }
  ]
}
```

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment

Ensure the frontend API base URL points to the backend:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the frontend

```bash
npm run dev
```

### 4. Use the chat interface

- Navigate to the chat page
- Type natural language commands:
  - "Add a task to buy groceries"
  - "Show my tasks"
  - "Mark buy groceries as done"
  - "Delete all completed tasks"

## Architecture Verification

After setup, verify the following:

- [ ] Backend starts without errors
- [ ] Database tables created (task, conversation, message)
- [ ] Chat endpoint returns agent responses
- [ ] MCP tools execute task operations
- [ ] Conversation persists across requests
- [ ] Frontend renders chat messages

## Troubleshooting

| Issue | Solution |
|---|---|
| `OPENAI_API_KEY` not set | Add to `.env` file |
| Database connection failed | Check `DATABASE_URL` in `.env` |
| MCP server not starting | Verify `mcp` package installed |
| Agent returns empty response | Check OpenAI API key and model availability |
