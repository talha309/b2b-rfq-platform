# POST /signup → Create a new user (customer, factory, or admin)
# POST /login → User login and token generation
# GET /profile → Get current user profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from models import models
from utils import schemas, util, validation
from database.data_base import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# signup
@auth_router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # check existing
    q = select(models.User).where(models.User.email == user_in.email)
    result = await db.execute(q)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = util.hash_password(user_in.password)
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# login
@auth_router.post("/login", response_model=schemas.Token)
async def login(form_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # login accepts email & password in body (UserCreate used for convenience)
    q = select(models.User).where(models.User.email == form_data.email)
    result = await db.execute(q)
    user = result.scalars().first()
    if not user or not util.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=validation.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = validation.create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

