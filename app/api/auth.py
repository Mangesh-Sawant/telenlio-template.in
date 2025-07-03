from datetime import timedelta
from uuid import uuid4

from app.core.security import hash_password, verify_password, create_access_token
from app.db.mongo import db
from app.models.user_model import UserCreate, UserInDB, LoginRequest
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/signup")
async def signup(user: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid4())
    hashed_pwd = hash_password(user.password)

    user_data = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_pwd,
        "name": user.name,
        "contact": user.contact,
        "surname": user.surname,
        "field": user.field
    }

    await db.users.insert_one(user_data)

    return {"message": "User created", "user_id": user_id}


@router.post("/login")
async def login(login_data: LoginRequest):
    user = await db.users.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["email"], "user_id": str(user["id"])},
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}
