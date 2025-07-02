from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: UUID = uuid4()
    email: EmailStr
    hashed_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
