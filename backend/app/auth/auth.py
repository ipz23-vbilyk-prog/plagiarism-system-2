from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal

from backend.app.models.user import User

from backend.app.auth.security import (
    hash_password,
    verify_password
)

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.username == username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = User(
        username=username,
        password=hash_password(password),
        role="user"
    )

    db.add(user)

    db.commit()

    return {
        "message": "User created"
    }


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(
        password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "message": "Login successful",
        "role": user.role
    }