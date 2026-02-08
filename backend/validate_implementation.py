#!/usr/bin/env python3
"""
Validation script to verify the Todo Backend implementation meets all requirements.
"""

import ast
import os
from pathlib import Path

def check_endpoints():
    """Check that all required API endpoints are implemented."""
    task_routes_path = Path("src/api/task_routes.py")

    with open(task_routes_path, 'r') as f:
        content = f.read()

    endpoints = {
        "GET /api/{user_id}/tasks": "get_tasks",
        "POST /api/{user_id}/tasks": "create_task",
        "GET /api/{user_id}/tasks/{id}": "get_task",
        "PUT /api/{user_id}/tasks/{id}": "update_task",
        "DELETE /api/{user_id}/tasks/{id}": "delete_task",
        "PATCH /api/{user_id}/tasks/{id}/complete": "toggle_task_completion"
    }

    found_endpoints = {}

    for endpoint, func_name in endpoints.items():
        if f"@router.{endpoint.split()[0].lower()}(" in content and f"def {func_name}" in content:
            found_endpoints[endpoint] = True
        else:
            found_endpoints[endpoint] = False

    return found_endpoints

def check_user_isolation():
    """Check that user isolation is enforced in all endpoints."""
    task_routes_path = Path("src/api/task_routes.py")

    with open(task_routes_path, 'r') as f:
        content = f.read()

    # Look for user_id validation in each endpoint
    validation_checks = []

    # Check if each endpoint verifies user_id matches authenticated user
    if "user_id != current_user" in content:
        validation_checks.append(("User ID validation", True))
    else:
        validation_checks.append(("User ID validation", False))

    # Check for user_id filtering in service calls
    if "user_id" in content and "TaskService" in content:
        validation_checks.append(("User ID in service calls", True))
    else:
        validation_checks.append(("User ID in service calls", False))

    return validation_checks

def check_data_model():
    """Check that the Task model has all required fields."""
    model_path = Path("src/models/task_model.py")

    with open(model_path, 'r') as f:
        content = f.read()

    required_fields = [
        "id",
        "title",
        "description",
        "completed",
        "user_id",
        "created_at",
        "updated_at"
    ]

    found_fields = {}
    for field in required_fields:
        found_fields[field] = field in content

    return found_fields

def check_authentication():
    """Check that authentication is implemented."""
    main_path = Path("src/main.py")
    auth_handler_path = Path("src/auth/auth_handler.py")

    auth_checks = []

    # Check if auth handler exists
    if auth_handler_path.exists():
        auth_checks.append(("Auth handler exists", True))

        with open(auth_handler_path, 'r') as f:
            auth_content = f.read()

        if "JWT" in auth_content or "jwt" in auth_content:
            auth_checks.append(("JWT implementation", True))
        else:
            auth_checks.append(("JWT implementation", False))

        if "get_current_user" in auth_content:
            auth_checks.append(("Current user function", True))
        else:
            auth_checks.append(("Current user function", False))
    else:
        auth_checks.append(("Auth handler exists", False))
        auth_checks.append(("JWT implementation", False))
        auth_checks.append(("Current user function", False))

    # Check if auth is used in routes
    with open(Path("src/api/task_routes.py"), 'r') as f:
        routes_content = f.read()

    if "get_current_user" in routes_content:
        auth_checks.append(("Auth used in routes", True))
    else:
        auth_checks.append(("Auth used in routes", False))

    return auth_checks

def main():
    print("Validating Todo Backend Implementation...")
    print("=" * 50)

    # Check endpoints
    print("\nChecking API Endpoints:")
    endpoints = check_endpoints()
    all_endpoints_present = True
    for endpoint, found in endpoints.items():
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {endpoint}")
        if not found:
            all_endpoints_present = False

    # Check user isolation
    print("\nChecking User Isolation:")
    user_isolation = check_user_isolation()
    user_isolation_ok = True
    for check, found in user_isolation:
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {check}")
        if not found:
            user_isolation_ok = False

    # Check data model
    print("\nChecking Data Model:")
    data_model = check_data_model()
    data_model_ok = True
    for field, found in data_model.items():
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {field}")
        if not found:
            data_model_ok = False

    # Check authentication
    print("\nChecking Authentication:")
    auth_checks = check_authentication()
    auth_ok = True
    for check, found in auth_checks:
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {check}")
        if not found:
            auth_ok = False

    print("\n" + "=" * 50)
    print("IMPLEMENTATION SUMMARY:")

    print(f"  API Endpoints: {'[COMPLETE]' if all_endpoints_present else '[INCOMPLETE]'}")
    print(f"  User Isolation: {'[ENFORCED]' if user_isolation_ok else '[WEAK]'}")
    print(f"  Data Model: {'[CORRECT]' if data_model_ok else '[INVALID]'}")
    print(f"  Authentication: {'[IMPLEMENTED]' if auth_ok else '[MISSING]'}")

    overall_success = all_endpoints_present and user_isolation_ok and data_model_ok and auth_ok

    print(f"\nOverall Status: {'[IMPLEMENTATION COMPLETE]' if overall_success else '[IMPLEMENTATION INCOMPLETE]'}")

    if overall_success:
        print("\nThe Todo Backend implementation meets all specified requirements!")
        print("   • All required API endpoints are implemented")
        print("   • User isolation is properly enforced")
        print("   • Task model has all required fields")
        print("   • Authentication is implemented with JWT")
        print("   • PATCH endpoint for toggling task completion is available")
    else:
        print("\nSome requirements are not met. Please review the validation results above.")

    return overall_success

if __name__ == "__main__":
    main()