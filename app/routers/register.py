# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.register import UserCreate, UserOut
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Steps:
    1) Validate username uniqueness
    2) Validate password byte length (bcrypt limit = 72 bytes)
    3) Hash the password
    4) Save user to database
    5) Return user data (without password)
    """

    # 1) Check if username already exists
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )

    # 2) IMPORTANT: bcrypt limit is 72 BYTES (UTF-8)
    password_bytes_len = len(payload.password.encode("utf-8"))
    if password_bytes_len > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long. bcrypt supports max 72 bytes (UTF-8)."
        )

    # 3) Hash password
    try:
        hashed = hash_password(payload.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # 4) Create and save user
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5) Return safe output
    return new_user
