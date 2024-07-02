import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import create_access_token, authenticate_user, router as auth_router
from app.config import get_db
from app.models import Base, engine
from app.schemas import OAuth2PasswordRequestFormCustom
from app.routes import pengguna, narapidana, izinkunjungan, suratpenahanan, kegiatanharian, pengunjung
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_pengguna

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestFormCustom = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, nomor_kepegawaian=form_data.nomor_kepegawaian, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nomor Kepegawaian atau Password Salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.nomor_kepegawaian})

    current_user = get_pengguna(db, user.nomor_kepegawaian)

    return {
        "Authorization": f"Bearer {access_token}",
        "detail": "Login Berhasil",
        "user": {
            "nomor_kepegawaian": current_user.nomor_kepegawaian,
            "nama": current_user.nama,
            "role": current_user.role,
        }
    }

app.include_router(auth_router)
app.include_router(kegiatanharian.router)
app.include_router(suratpenahanan.router)
app.include_router(pengguna.router)
app.include_router(narapidana.router)
app.include_router(izinkunjungan.router)
app.include_router(pengunjung.router)
