from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    contact: int
    surname: str
    field: str


class UserInDB(BaseModel):
    id: UUID = uuid4()
    email: EmailStr
    hashed_password: str
    contact_name: str
    surname: str
    field: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
