from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..security import create_token, decode_username, verify_password

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel): username: str; password: str

def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    username = decode_username(token)
    user = db.scalar(select(User).where(User.username == username)) if username else None
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录已失效")
    return user

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == payload.username))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"access_token": create_token(user.username), "token_type": "bearer", "username": user.username}

@router.get("/me")
def me(user: User = Depends(current_user)): return {"username": user.username}

@router.get("/accounts")
def accounts(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [{"username": item.username} for item in db.scalars(select(User).order_by(User.username)) if item.id != user.id]
