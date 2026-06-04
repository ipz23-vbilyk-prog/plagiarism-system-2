from fastapi import Header, HTTPException
from jose import jwt, JWTError

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"

# ==========================================
# USERS DATABASE
# ==========================================

users_db = [
    {
        "id": 1,
        "email": "admin@admin.com",
        "password": "admin",
        "role": "admin"
    }
]

# ==========================================
# CREATE TOKEN
# ==========================================

def create_access_token(data: dict):

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ==========================================
# VERIFY TOKEN
# ==========================================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None

# ==========================================
# CURRENT USER
# ==========================================

def get_current_user(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token not provided"
        )

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        payload = verify_token(token)

        if not payload:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        email = payload.get("sub")

        for user in users_db:

            if user["email"] == email:

                return user

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

# ==========================================
# ADMIN CHECK
# ==========================================

def require_admin(
    user=Header(None)
):

    current_user = get_current_user(user)

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user