from app.auth import get_current_user
from app.config import get_db
from app.models import IzinKunjungan, Pengunjung
from app.schemas import PengunjungBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pengunjung", tags=['pengunjung'])


@router.post("/create-pengunjung", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)])
async def create_pengunjung(pengunjung: PengunjungBase, db: Session = Depends(get_db)):
    db_izin = db.query(IzinKunjungan).filter(IzinKunjungan.nomor_izin == pengunjung.nomor_izin).first()
    if not db_izin:
        raise HTTPException(status_code=404, detail="Izin Kunjungan Tidak Ditemukan")

    db_pengunjung = Pengunjung(**pengunjung.dict())
    db.add(db_pengunjung)
    db.commit()
    db.refresh(db_pengunjung)
    return {'detail': 'RESULT_OK'}


@router.get("/get-pengunjung", dependencies=[Depends(get_current_user)])
async def get_all_pengunjung(db: Session = Depends(get_db)):
    return db.query(Pengunjung).all()


@router.get("/get-pengunjung/{id_pengunjung}", response_model=PengunjungBase, dependencies=[Depends(get_current_user)])
async def get_pengunjung(id_pengunjung: int, db: Session = Depends(get_db)):
    pengunjung = db.query(Pengunjung).filter(Pengunjung.id_pengunjung == id_pengunjung).first()
    if not pengunjung:
        raise HTTPException(status_code=404, detail="Pengunjung Tidak Ditemukan")
    return pengunjung


@router.put("/update-pengunjung/{id_pengunjung}", dependencies=[Depends(get_current_user)])
async def update_pengunjung(id_pengunjung: int, pengunjung: PengunjungBase, db: Session = Depends(get_db)):
    db_pengunjung = db.query(Pengunjung).filter(Pengunjung.id_pengunjung == id_pengunjung).first()
    if not db_pengunjung:
        raise HTTPException(status_code=404, detail="Pengunjung Tidak Ditemukan")

    db_izin = db.query(IzinKunjungan).filter(IzinKunjungan.nomor_izin == pengunjung.nomor_izin).first()
    if not db_izin:
        raise HTTPException(status_code=404, detail="Izin Kunjungan Tidak Ditemukan")

    db_pengunjung.nama_pengunjung = pengunjung.nama_pengunjung
    db_pengunjung.nomor_izin = pengunjung.nomor_izin
    db.commit()
    db.refresh(db_pengunjung)
    return {'detail': 'RESULT_OK'}


@router.delete("/delete-pengunjung/{id_pengunjung}", dependencies=[Depends(get_current_user)])
async def delete_pengunjung(id_pengunjung: int, db: Session = Depends(get_db)):
    db_pengunjung = db.query(Pengunjung).filter(Pengunjung.id_pengunjung == id_pengunjung).first()
    if not db_pengunjung:
        raise HTTPException(status_code=404, detail="Pengunjung Tidak Ditemukan")
    db.delete(db_pengunjung)
    db.commit()
    return {"detail": 'RESULT_OK'}
