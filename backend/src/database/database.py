from sqlmodel import SQLModel, create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
import os
from typing import Optional
import urllib.parse

# Import models to ensure they are registered with SQLModel
from ..models.user_model import User
from ..models.task_model import Task
from ..models.conversation_model import Conversation
from ..models.message_model import Message

# Get database URL from environment or use SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# For PostgreSQL, we need to handle special characters in the URL
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgresql+psycopg2://"):
    # Parse and re-encode the URL to handle special characters properly
    parsed = urllib.parse.urlparse(DATABASE_URL)
    if parsed.password:
        # Reconstruct URL with properly encoded password
        encoded_password = urllib.parse.quote_plus(parsed.password)
        DATABASE_URL = f"{parsed.scheme}://{parsed.username}:{encoded_password}@{parsed.hostname}:{parsed.port}{parsed.path}"

# Create engine with appropriate settings based on database type
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
else:
    engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    """
    Creates the database tables.
    This should be called when starting the application.
    """
    SQLModel.metadata.create_all(engine)

# For PostgreSQL, enable foreign key constraints which are on by default in SQLite
if DATABASE_URL.startswith("postgresql"):
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()