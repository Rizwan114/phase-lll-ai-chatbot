# Quickstart Guide: Authentication & Security Implementation

## Overview
This guide walks through implementing JWT-based authentication for the Todo Full-Stack Web Application with Better Auth on the frontend and FastAPI middleware on the backend.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.9+ for backend development
- Better Auth configured in the Next.js frontend
- Shared JWT secret between frontend and backend services

## Step-by-Step Implementation

### Step 1: Configure JWT Settings
1. Set up JWT secret in environment variables for both frontend and backend
2. Define JWT expiration time (recommended: 24 hours)
3. Configure token claims to include `user_id` field

### Step 2: Implement Frontend Auth Client
1. Integrate Better Auth into Next.js application
2. Create API client that automatically attaches JWT to requests
3. Implement token refresh and error handling

### Step 3: Create Backend JWT Middleware
1. Develop FastAPI dependency for JWT validation
2. Implement user identity extraction from tokens
3. Create middleware to verify user_id matches route parameter

### Step 4: Update Existing Endpoints
1. Add authentication dependencies to all existing task endpoints
2. Implement user isolation checks in service layer
3. Update error handling for unauthorized access

### Step 5: Test Authentication Flow
1. Register a new user through frontend
2. Verify JWT token generation and storage
3. Test API access with valid and invalid tokens
4. Verify user isolation (cannot access other users' tasks)

## Testing Commands

### Backend Testing
```bash
# Start backend with auth-enabled endpoints
cd backend && uvicorn src.main:app --reload

# Test unauthenticated access (should return 401)
curl -X GET http://localhost:8000/api/user123/tasks

# Test authenticated access with valid JWT
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -X GET http://localhost:8000/api/YOUR_USER_ID/tasks
```

### Frontend Testing
```bash
# Start frontend application
cd frontend && npm run dev

# Visit the application and test:
# 1. User registration and login
# 2. Task creation with authenticated session
# 3. Access to existing tasks
# 4. Logout functionality
```

## Verification Checklist

- [ ] All API endpoints return 401 for unauthenticated requests
- [ ] Valid JWT tokens allow access to matching user resources
- [ ] Invalid user_id mismatch returns 403 forbidden
- [ ] Cross-user access attempts are blocked
- [ ] JWT token expiration is properly handled
- [ ] Error messages don't reveal internal user mappings
- [ ] End-to-end flow works: signup → login → CRUD tasks → logout

## Troubleshooting

### Common Issues
1. **401 Unauthorized for valid tokens**: Check JWT secret is identical in frontend and backend
2. **Cross-user access allowed**: Verify user_id comparison in middleware
3. **Token not attaching to requests**: Check frontend API client implementation
4. **Expired token not handled**: Implement proper error catching and re-authentication

### Security Verification
1. Test with malformed JWT tokens (should return 401)
2. Test with expired tokens (should return 401)
3. Test with tampered signature (should return 401)
4. Test user_id parameter manipulation (should return 403 or 404)