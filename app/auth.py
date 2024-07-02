import logging
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models
from app.config import get_db

SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 900

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

# Set untuk menampung token yang di-blacklist
blacklisted_tokens = set()

def blacklist_token(token: str):
    blacklisted_tokens.add(token)

def is_token_blacklisted(token: str):
    return token in blacklisted_tokens

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

print(hash_password("123456"))

def get_pengguna(db: Session, nomor_kepegawaian: str):
    return db.query(models.Pengguna).filter(models.Pengguna.nomor_kepegawaian == nomor_kepegawaian).first()

def authenticate_user(db: Session, nomor_kepegawaian: str, password: str):
    user = get_pengguna(db, nomor_kepegawaian)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    user.is_active = True
    db.commit()
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Sudah Tidak Berlaku",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(token.credentials)
    nomor_kepegawaian: str = payload.get("sub")
    if nomor_kepegawaian is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nomor Pegawai Tidak Ditemukan",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_pengguna(db, nomor_kepegawaian)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_user(current_user: models.Pengguna = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_admin_user(current_user: models.Pengguna = Depends(get_current_active_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

def get_current_staff_user(current_user: models.Pengguna = Depends(get_current_active_user)):
    if current_user.role not in ['admin', 'staff_lapas']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

# Router untuk logout
router = APIRouter()

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklist_token(token.credentials)
    return {"detail": "Logged out"}
