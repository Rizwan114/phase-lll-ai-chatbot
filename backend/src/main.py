from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api import task_routes, auth_routes, chat_routes
from .database.database import create_db_and_tables
from .handlers.auth_errors import unauthorized_exception_handler, forbidden_exception_handler
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from fastapi import HTTPException as FastAPIHTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Todo Backend API",
    description="AI-powered Todo Chatbot API with MCP tools and natural language task management",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(task_routes.router, prefix="/api", tags=["tasks"])
app.include_router(chat_routes.router, prefix="/api", tags=["chat"])

# Add custom exception handler that preserves original status codes
def custom_http_exception_handler(request, exc):
    """Route HTTP exceptions to appropriate handlers based on status code"""
    if exc.status_code == 401:
        return unauthorized_exception_handler(request, exc)
    if exc.status_code == 403:
        return forbidden_exception_handler(request, exc)
    # For all other status codes, return standard JSON response
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.add_exception_handler(FastAPIHTTPException, custom_http_exception_handler)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}