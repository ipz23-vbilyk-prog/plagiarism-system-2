from jose import jwt, JWTError
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        if email is None:
            raise HTTPException(status_code=401)

        return {"email": email, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")