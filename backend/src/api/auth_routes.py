from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from ..database.database import engine
from ..auth.auth_handler import create_access_token
from ..models.user_model import User
from ..utils.logger import log_info, log_error

router = APIRouter()


class LoginRequest(BaseModel):
    user_id: str
    password: str


class SignupRequest(BaseModel):
    user_id: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    user_id: str
    token_type: str = "bearer"


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest):
    """
    Authenticate a user and return a JWT token.
    For this hackathon demo, password validation is simplified.
    """
    user_id = request.user_id.strip()
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )

    if not request.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required",
        )

    # Check if user exists
    with Session(engine) as session:
        from sqlmodel import select

        stmt = select(User).where(User.user_id == user_id)
        user = session.exec(stmt).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

    # Create JWT token with user_id as subject
    token = create_access_token(data={"sub": user_id, "user_id": user_id})

    log_info(f"User logged in", extra={"user_id": user_id})

    return AuthResponse(access_token=token, user_id=user_id)


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest):
    """
    Register a new user and return a JWT token.
    """
    user_id = request.user_id.strip()
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )

    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    with Session(engine) as session:
        from sqlmodel import select

        # Check if user already exists
        stmt = select(User).where(User.user_id == user_id)
        existing = session.exec(stmt).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User ID already exists",
            )

        # Create new user
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    # Create JWT token
    token = create_access_token(data={"sub": user_id, "user_id": user_id})

    log_info(f"User registered", extra={"user_id": user_id})

    return AuthResponse(access_token=token, user_id=user_id)
