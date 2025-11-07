# utils/deps.py
from fastapi import Depends, HTTPException, status
from utils.validation import get_current_user  # your JWT decode function

def admin_required(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
