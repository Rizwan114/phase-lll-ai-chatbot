# Quickstart: AI Agent, MCP Orchestration & Frontend Integration

**Branch**: `005-agent-mcp-integration` | **Date**: 2026-02-11

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon) database with connection string
- OpenAI API key

## Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env: set DATABASE_URL, OPENAI_API_KEY, SECRET_KEY
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Backend runs at `http://localhost:8000`.

## Frontend Setup

```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 in .env.local
npm run dev
```

Frontend runs at `http://localhost:3000`.

## Verify End-to-End Flow

1. **Sign up**: Navigate to `http://localhost:3000/signup`
2. **Log in**: Navigate to `http://localhost:3000/login`
3. **Open chat**: Navigate to `http://localhost:3000/chat`
4. **Send message**: Type "Add buy groceries" and send
5. **Verify response**: Agent should confirm task was added
6. **List tasks**: Type "Show my tasks"
7. **Complete task**: Type "Mark buy groceries as done"
8. **Multi-step**: Type "Delete all completed tasks"

## API Quick Test (curl)

```bash
# Get JWT token (sign up or log in first via frontend)
TOKEN="your-jwt-token"
USER_ID="your-user-id"

# Send chat message
curl -X POST "http://localhost:8000/api/${USER_ID}/chat" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries"}'

# Load conversation history
curl -X GET "http://localhost:8000/api/${USER_ID}/chat/history" \
  -H "Authorization: Bearer ${TOKEN}"
```

## Verification Checklist

- [ ] Agent adds task when asked "Add buy groceries"
- [ ] Agent lists tasks when asked "Show my tasks"
- [ ] Agent completes task when asked "Mark X as done"
- [ ] Agent deletes task when asked "Delete X"
- [ ] Agent performs multi-step: "Delete all completed tasks"
- [ ] Conversation persists across page reloads
- [ ] Tool call metadata visible in frontend
- [ ] Empty message is rejected
- [ ] Non-task requests get conversational response
- [ ] Error messages are user-friendly
