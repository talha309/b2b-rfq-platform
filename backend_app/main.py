from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

from database.data_base import  Base, get_db
from routes.authentication_routes import auth_router
from models import models
from utils import validation, schemas

app = FastAPI(title="FastAPI Auth Example")

# include router
app.include_router(auth_router.router)

# Simple dependency to get current user from bearer token
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    try:
        token_data = validation.decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    q = select(models.User).where(models.User.id == token_data.user_id)
    result = await db.execute(q)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.get("/me", response_model=schemas.UserOut)
async def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user
