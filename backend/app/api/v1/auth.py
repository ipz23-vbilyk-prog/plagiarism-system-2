from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.core.auth import (
    users_db,
    create_access_token
)

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(data: RegisterRequest):

    for user in users_db:

        if user["email"] == data.email:

            raise HTTPException(
                status_code=400,
                detail="Пользователь уже существует"
            )

    users_db.append(
        {
            "id": len(users_db) + 1,
            "email": data.email,
            "password": data.password,
            "role": "user"
        }
    )

    return {
        "success": True,
        "message": "Регистрация выполнена"
    }


@router.post("/login")
async def login(data: LoginRequest):

    for user in users_db:

        if (
            user["email"] == data.email
            and
            user["password"] == data.password
        ):

            token = create_access_token(
                {
                    "sub": user["email"]
                }
            )

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }

    raise HTTPException(
        status_code=401,
        detail="Неверный email или пароль"
    )