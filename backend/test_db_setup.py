#!/usr/bin/env python3
"""
Simple test to verify database models and connections work correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    # Test basic imports
    from src.models.user_model import User
    from src.models.task_model import Task
    print("✅ Models imported successfully")

    # Test database connection
    from src.database.database import engine, create_db_and_tables
    print("✅ Database engine created successfully")

    # Test table creation
    create_db_and_tables()
    print("✅ Tables created successfully")

    print("🎉 All database components working correctly!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()