# POST /signup → Create a new user (customer, factory, or admin)
# POST /login → User login and token generation
# GET /profile → Get current user profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import User
from utils.schemas import UserCreate, UserLogin, Token, UserOut
from database.data_base import get_db
from utils.util import hash_password, verify_password, create_access_token
from utils.validation import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# ✅ Protected route (requires token)
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Return current logged-in user's info."""
    return current_user
