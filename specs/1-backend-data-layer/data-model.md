# Data Model: Core Backend & Data Layer for Todo Full-Stack Web Application

## Entity: Task

**Description**: Represents a user's task with properties like title, description, completion status, timestamps, and associated user_id

**Fields**:
- `id`: Primary key, auto-generated integer/UUID
- `title`: String, required, maximum length 255 characters
- `description`: String, optional, maximum length 1000 characters
- `completed`: Boolean, default False
- `user_id`: String or UUID, required, foreign key reference to user
- `created_at`: DateTime, auto-generated timestamp
- `updated_at`: DateTime, auto-generated timestamp that updates on modification

**Validation Rules**:
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- user_id must be a valid identifier format
- completed field must be boolean type
- created_at and updated_at are automatically managed by the system

**Relationships**:
- One-to-many relationship with User entity (one user can have many tasks)
- All queries must be scoped by user_id to ensure proper access control

**State Transitions**:
- Task is created with completed=False
- Task can transition to completed=True via update operation
- Task can transition back to completed=False via update operation
- Task can be deleted (removed from system)

## Entity: User

**Description**: Represents a user in the system with unique identifier (user_id) that owns tasks

**Fields**:
- `user_id`: String or UUID, required, unique identifier
- `created_at`: DateTime, auto-generated timestamp
- `updated_at`: DateTime, auto-generated timestamp that updates on modification

**Validation Rules**:
- user_id must be unique across the system
- user_id must be a valid identifier format
- created_at and updated_at are automatically managed by the system