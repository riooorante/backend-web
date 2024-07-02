from app.auth import get_current_user
from app.config import get_db
from app.models import KegiatanHarian, Pengguna
from app.schemas import KegiatanHarianBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/kegiatan-harian", tags=['kegiatan-harian'])


@router.post("/create-kegiatan-harian", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_kegiatan_harian(kegiatan_harian: KegiatanHarianBase, db: Session = Depends(get_db)):
    try:
        db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == kegiatan_harian.penanggung_jawab).first()
        if db_pengguna is None:
            raise HTTPException(status_code=404, detail='Staff Lapas Tidak Ditemukan!')

        db_kegiatan_harian = KegiatanHarian(**kegiatan_harian.dict())
        db.add(db_kegiatan_harian)
        db.commit()
        return {'detail': 'RESULT_OK'}
    except Exception as e:
        raise HTTPException(status_code=500, detail='Gagal Menambahkan Kegiatan Harian Baru!')


# Read all
@router.get("/get-kegiatan-harian", dependencies=[Depends(get_current_user)])
async def get_all_kegiatan_harian(db: Session = Depends(get_db)):
    return db.query(KegiatanHarian).all()


# Read
@router.get("/get-kegiatan-harian/{nomor_kegiatan}", dependencies=[Depends(get_current_user)])
async def get_kegiatan_harian(nomor_kegiatan: str, db: Session = Depends(get_db)):
    kegiatan_harian = db.query(KegiatanHarian).filter(KegiatanHarian.nomor_kegiatan == nomor_kegiatan).first()
    if kegiatan_harian is None:
        raise HTTPException(status_code=404, detail='Kegiatan Harian Tidak Ditemukan!')
    return kegiatan_harian


# Update
@router.put("/update-kegiatan-harian/{nomor_kegiatan}", dependencies=[Depends(get_current_user)])
async def update_kegiatan_harian(nomor_kegiatan: str, kegiatan_harian: KegiatanHarianBase,
                                 db: Session = Depends(get_db)):
    db_kegiatan_harian = db.query(KegiatanHarian).filter(KegiatanHarian.nomor_kegiatan == nomor_kegiatan).first()
    if db_kegiatan_harian is None:
        raise HTTPException(status_code=404, detail='Kegiatan Harian Tidak Ditemukan!')

    db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == kegiatan_harian.penanggung_jawab).first()
    if db_pengguna is None:
        raise HTTPException(status_code=404, detail='Staff Lapas Tidak Ditemukan!')

    if db_pengguna.role == "admin":
        raise HTTPException(status_code=403, detail='Role tidak diizinkan!')

    db_kegiatan_harian.tanggal_kegiatan = kegiatan_harian.tanggal_kegiatan
    db_kegiatan_harian.deskripsi_kegiatan = kegiatan_harian.deskripsi_kegiatan
    db_kegiatan_harian.lokasi = kegiatan_harian.lokasi
    db_kegiatan_harian.penanggung_jawab = kegiatan_harian.penanggung_jawab
    db.commit()
    return {'detail': 'RESULT_OK'}


# Delete
@router.delete("/delete-kegiatan-harian/{nomor_kegiatan}", dependencies=[Depends(get_current_user)])
async def delete_kegiatan_harian(nomor_kegiatan: str, db: Session = Depends(get_db)):
    db_kegiatan_harian = db.query(KegiatanHarian).filter(KegiatanHarian.nomor_kegiatan == nomor_kegiatan).first()
    if db_kegiatan_harian is None:
        raise HTTPException(status_code=404, detail="Kegiatan Harian tidak ditemukan!")
    db.delete(db_kegiatan_harian)
    db.commit()
    return {"detail": 'RESULT_OK'}
