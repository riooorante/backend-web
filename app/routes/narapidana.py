from app.auth import get_current_user
from app.config import get_db
from app.models import Narapidana
from app.schemas import NarapidanaBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/narapidana", tags=['narapidana'])


@router.post("/create-narapidana", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_narapidana(narapidana: NarapidanaBase, db: Session = Depends(get_db)) -> dict:
    try:
        db_narapidana = Narapidana(**narapidana.dict())
        db.add(db_narapidana)
        db.commit()
        return {'detail': 'RESULT_OK'}
    except Exception as e:
        raise HTTPException(status_code=500, detail='Gagal Menambahkan Narapidana Baru!')


@router.get("/get-narapidana", dependencies=[Depends(get_current_user)])
async def get_all_narapidana(db: Session = Depends(get_db)):
    return db.query(Narapidana).all()


@router.get("/get-narapidana/{nomor_narapidana}", dependencies=[Depends(get_current_user)])
async def get_narapidana(nomor_narapidana: str, db: Session = Depends(get_db)):
    try:
        narapidana = db.query(Narapidana).filter(Narapidana.nomor_narapidana == nomor_narapidana).first()
        if narapidana is None:
            raise HTTPException(status_code=404, detail='Narapidana Tidak Ditemukan!')
        return narapidana
    finally:
        db.close()


@router.put("/update-narapidana/{nomor_narapidana}", dependencies=[Depends(get_current_user)])
async def update_narapidana(nomor_narapidana: str, narapidana: NarapidanaBase, db: Session = Depends(get_db)):
    db_narapidana = db.query(Narapidana).filter(Narapidana.nomor_narapidana == nomor_narapidana).first()
    if db_narapidana is None:
        raise HTTPException(status_code=404, detail='Narapidana Tidak Ditemukan!')
    db_narapidana.nomor_narapidana = narapidana.nomor_narapidana
    db_narapidana.nama = narapidana.nama
    db_narapidana.tanggal_masuk = narapidana.tanggal_masuk
    db_narapidana.tanggal_lahir = narapidana.tanggal_lahir
    db_narapidana.deskripsi_kasus = narapidana.deskripsi_kasus
    db_narapidana.nomor_kamar = narapidana.nomor_kamar

    return {'detail': 'RESULT_OK'}


@router.delete("/delete-narapidana/{nomor_narapidana}", dependencies=[Depends(get_current_user)])
async def delete_prodi(nomor_narapidana: str, db: Session = Depends(get_db)):
    db_narapidana = db.query(Narapidana).filter(Narapidana.nomor_narapidana == nomor_narapidana).first()
    if db_narapidana is None:
        raise HTTPException(status_code=404, detail="Narapidana tidak ditemukan!")
    nama_narapidana = db_narapidana.nama
    db.delete(db_narapidana)
    db.commit()
    return {"detail": 'RESULT_OK'}
