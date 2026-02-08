# Implementation Plan: Authentication & Security Layer for Todo Full-Stack Web Application

**Feature**: [2-auth-security/spec.md](spec.md)
**Created**: 2026-02-06
**Status**: Draft
**Author**: Claude Code
**Branch**: 2-auth-security

## Overview

This plan outlines the implementation of JWT-based authentication and security features for the Todo Full-Stack Web Application. The focus is on integrating Better Auth with the frontend and implementing JWT verification middleware in the FastAPI backend to ensure proper user isolation and authorization.

## Technical Context

- **Frontend Framework**: Next.js 16+ (App Router)
- **Backend Framework**: Python FastAPI
- **Authentication**: Better Auth + JWT tokens
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **API Protocol**: REST with JWT Authorization headers
- **Architecture**: Stateful frontend with stateless backend authentication

### Technology Stack Alignment
- [X] Frontend: Next.js 16+ (App Router)
- [X] Backend: Python FastAPI
- [X] Authentication: Better Auth + JWT
- [X] ORM: SQLModel
- [X] Database: Neon Serverless PostgreSQL

### Known Unknowns
- JWT payload fields required by backend - [RESOLVED in research.md: JWT tokens will include standard claims (sub, exp, iat) plus custom user_id claim]
- Token expiration duration and validation rules - [RESOLVED in research.md: 24-hour expiration with stateless validation]
- Strategy for matching JWT user identity with route user_id - [RESOLVED in research.md: Middleware compares user_id claim in JWT with user_id parameter in route path]

### Dependencies
- Frontend: Better Auth library for user authentication
- Backend: python-jose for JWT operations, FastAPI middleware
- Shared: Common JWT secret between frontend and backend
- Database: Integration with existing task model for user isolation

## Constitution Check

### Spec-First Development
- [X] All functionality mapped to spec requirements
- [X] Implementation follows approved spec requirements (FR-001 through FR-010)

### Correctness and Consistency
- [X] API behavior matches defined REST contract
- [X] Frontend and backend integration planned with shared JWT secret
- [ ] API consistency validated post-implementation

### Security-by-Design
- [X] Authentication enforced at all API boundaries
- [X] Data isolation planned for cross-user access prevention
- [X] Secret handling via environment variables (no hardcoding)

### Automation Over Manual Work
- [X] Code generation planned via Claude Code
- [X] No manual coding outside agent-generated outputs

### Tech Stack Compliance
- [X] Using Better Auth + JWT for authentication
- [X] Using FastAPI for backend JWT verification
- [X] Maintaining existing tech stack

### Quality and Validation Standards
- [X] Planning for 401 Unauthorized responses for unauthenticated requests
- [X] Shared secret implementation across services
- [X] Multi-user isolation in database schema
- [X] JWT attachment to every API request from frontend

## Gates

### Gate 1: Design Completeness
- [X] All known unknowns resolved
- [X] Detailed API contracts defined
- [X] Security architecture validated

### Gate 2: Implementation Feasibility
- [X] All dependencies identified and available
- [X] Integration points with existing backend verified
- [X] Performance implications assessed

### Gate 3: Security Validation
- [X] JWT token handling reviewed for security
- [X] User isolation mechanisms validated
- [X] Secret management procedures confirmed

## Phase 0: Research & Architecture

### R0.1: JWT Architecture Research
**Research Task**: Investigate JWT implementation patterns for Next.js + FastAPI integration

**Decision**: JWT payload structure and claims for user identification
**Rationale**: Need standardized claims for consistent user identity verification
**Alternatives considered**:
- Simple user_id claim vs richer user profile
- Custom claims vs standard JWT claims
- Signed vs encrypted tokens

### R0.2: Better Auth Integration Research
**Research Task**: Best practices for Better Auth integration with Next.js frontend

**Decision**: Frontend authentication flow and token management
**Rationale**: Better Auth provides established patterns for JWT handling
**Alternatives considered**:
- Self-implemented JWT creation vs Better Auth
- Cookie-based vs header-based token transmission

### R0.3: FastAPI JWT Middleware Research
**Research Task**: Optimal JWT verification middleware implementation for FastAPI

**Decision**: Stateless JWT validation approach
**Rationale**: Maintains scalability and aligns with spec requirements
**Alternatives considered**:
- Database lookup vs stateless validation
- Custom middleware vs existing libraries

### R0.4: Token Expiration Strategy Research
**Research Task**: Appropriate JWT expiration duration for security and UX balance

**Decision**: Token expiration and validation rules
**Rationale**: Balance security (shorter tokens) with user experience (longer sessions)
**Alternatives considered**:
- Short-lived tokens (15-30 min) vs long-lived tokens (days)
- Refresh token implementation vs simple re-authentication

## Phase 1: Data Model & Contracts

### P1.1: Enhanced User Identity Model
Create data-model.md defining JWT claims and user identity structures

**Requirements**:
- JWT token structure with user_id claim
- Token validation schema
- User session state representation

### P1.2: API Contract Design
Define API contracts in /contracts/ for authentication endpoints

**Endpoints**:
- `/auth/login` - Login and JWT token issuance
- `/auth/signup` - Registration and JWT token issuance
- All existing task endpoints to accept JWT tokens

### P1.3: Security Contract Definition
Specify security requirements for all existing API endpoints

**Requirements**:
- All task endpoints require Authorization header
- User isolation verification mechanism
- Error response contracts for unauthorized access

## Phase 2: Implementation Architecture

### P2.1: Frontend Auth Flow Implementation
**Component**: `frontend/src/lib/auth/`

**Files**:
- `auth-client.ts` - Better Auth integration and token management
- `api-client.ts` - HTTP client that attaches JWT to requests
- `middleware.ts` - Next.js middleware for auth protection

**Functionality**:
- User authentication via Better Auth
- Automatic JWT token attachment to API requests
- Token refresh handling

### P2.2: Backend JWT Verification Middleware
**Component**: `backend/src/auth/`

**Files**:
- `auth_handler.py` - JWT decoding and validation logic
- `middleware.py` - FastAPI dependency for auth verification
- `config.py` - JWT settings and secret configuration

**Functionality**:
- Stateless JWT token validation using shared secret
- User identity extraction from token claims
- 401 response for invalid/missing tokens

### P2.3: User Isolation Enhancement
**Component**: `backend/src/services/task_service.py`

**Enhancements**:
- User ID validation in all task operations
- Route-level user verification against JWT claims
- Proper error responses for cross-user access attempts

### P2.4: Frontend API Client Integration
**Component**: `frontend/src/lib/api/`

**Files**:
- `task-api.ts` - Task API client with automatic JWT attachment
- `auth-interceptor.ts` - Interceptor for handling auth errors

**Functionality**:
- Automatic inclusion of Authorization header
- Proper error handling for 401 responses
- Token refresh upon expiration

## Phase 3: Integration & Validation

### P3.1: Frontend-Backend Integration Testing
- Verify JWT token generation and validation across services
- Test user isolation with cross-user access attempts
- Validate 401 responses for unauthenticated requests

### P3.2: Security Penetration Testing
- Attempt access to other users' tasks
- Test invalid/expired token handling
- Verify proper error responses

### P3.3: End-to-End User Flow Validation
- Complete user journey: signup → login → CRUD tasks → logout
- Verify JWT token persistence and usage
- Confirm all API endpoints properly secured

## Quickstart Guide

### Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- Better Auth configured for frontend
- Shared JWT secret configured in both services

### Setup Instructions
1. Configure Better Auth in Next.js frontend
2. Set JWT secret in both frontend and backend environments
3. Update backend to require JWT for all task endpoints
4. Configure frontend API client to attach JWT tokens
5. Test authentication flow and user isolation

### Running the Application
1. Start backend: `cd backend && uvicorn src.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Visit frontend and register/login to test auth flow

## Security Considerations

- **JWT Secret Management**: Store in environment variables, never hardcode
- **Token Expiration**: Implement appropriate expiration times
- **User Isolation**: Always verify user_id in JWT matches route/user context
- **Error Messages**: Don't expose internal user mapping in error responses
- **Transport Security**: All JWT tokens must be sent over HTTPS

## Performance Impact

- JWT validation adds minimal overhead (< 10ms)
- Stateless validation avoids database lookups for token validation
- Caching mechanisms may be implemented for high-traffic scenarios
- Memory footprint increase due to token validation logic

## Rollback Plan

If security issues arise:
1. Disable authentication temporarily to maintain functionality
2. Revert to the previous non-authenticated backend state
3. Remove JWT validation from all endpoints
4. Restore previous access patterns while investigating