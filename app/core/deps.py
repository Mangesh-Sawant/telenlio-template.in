from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from app.core import security  # this imports your existing secret + JWT logic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # update if your login route is different

class TokenData(BaseModel):
    email: str
    user_id: str

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
        return TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception
