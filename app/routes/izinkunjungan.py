from app.auth import get_current_user
from app.config import get_db
from app.models import Pengguna, Narapidana, IzinKunjungan
from app.schemas import IzinKunjunganBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/izin-kunjungan", tags=['izinkunjungan'])


@router.post("/create-izin-kunjungan", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)])
async def create_izin_kunjungan(izin_kunjungan: IzinKunjunganBase, db: Session = Depends(get_db)):
    try:
        db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == izin_kunjungan.penanggung_jawab).first()
        if db_pengguna is None:
            raise HTTPException(status_code=404, detail='Staff Lapas Tidak Ditemukan!')

        db_narapidana = db.query(Narapidana).filter(
            Narapidana.nomor_narapidana == izin_kunjungan.nomor_narapidana).first()
        if db_narapidana is None:
            raise HTTPException(status_code=404, detail='Narapidana Tidak Ditemukan!')

        db_izin_kunjungan = IzinKunjungan(**izin_kunjungan.dict())
        db.add(db_izin_kunjungan)
        db.commit()
        return {'detail': 'RESULT_OK'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


@router.get("/get-izin-kunjungan", dependencies=[Depends(get_current_user)])
async def get_all_izin_kunjungan(db: Session = Depends(get_db)):
    return db.query(IzinKunjungan).all()


@router.get("/get-izin-kunjungan/{nomor_izin}", dependencies=[Depends(get_current_user)])
async def get_izin_kunjungan(nomor_izin: str, db: Session = Depends(get_db)):
    izin_kunjungan = db.query(IzinKunjungan).filter(IzinKunjungan.nomor_izin == nomor_izin).first()
    if izin_kunjungan is None:
        raise HTTPException(status_code=404, detail='Izin Kunjungan Tidak Ditemukan!')
    return izin_kunjungan


@router.put("/update-izin-kunjungan/{nomor_izin}", dependencies=[Depends(get_current_user)])
async def update_izin_kunjungan(nomor_izin: str, izin_kunjungan: IzinKunjunganBase, db: Session = Depends(get_db)):
    db_izin_kunjungan = db.query(IzinKunjungan).filter(IzinKunjungan.nomor_izin == nomor_izin).first()
    if db_izin_kunjungan is None:
        raise HTTPException(status_code=404, detail='Izin Kunjungan Tidak Ditemukan!')

    db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == izin_kunjungan.penanggung_jawab).first()
    if db_pengguna is None:
        raise HTTPException(status_code=404, detail='Staff Lapas Tidak Ditemukan!')

    db_narapidana = db.query(Narapidana).filter(Narapidana.nomor_narapidana == izin_kunjungan.nomor_narapidana).first()
    if db_narapidana is None:
        raise HTTPException(status_code=404, detail='Narapidana Tidak Ditemukan!')

    db_izin_kunjungan.waktu_kunjungan = izin_kunjungan.waktu_kunjungan
    db_izin_kunjungan.keterangan = izin_kunjungan.keterangan
    db_izin_kunjungan.penanggung_jawab = izin_kunjungan.penanggung_jawab
    db_izin_kunjungan.nomor_narapidana = izin_kunjungan.nomor_narapidana
    db.commit()
    return {'detail': 'RESULT_OK'}


@router.delete("/delete-izin-kunjungan/{nomor_izin}", dependencies=[Depends(get_current_user)])
async def delete_izin_kunjungan(nomor_izin: str, db: Session = Depends(get_db)):
    db_izin_kunjungan = db.query(IzinKunjungan).filter(IzinKunjungan.nomor_izin == nomor_izin).first()
    if db_izin_kunjungan is None:
        raise HTTPException(status_code=404, detail="Izin Kunjungan tidak ditemukan!")
    db.delete(db_izin_kunjungan)
    db.commit()
    return {"detail": 'RESULT_OK'}
