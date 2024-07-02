from app.auth import get_current_user
from app.config import get_db
from app.models import Narapidana, SuratPerintahPenahanan
from app.schemas import SuratPerintahPenahananBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/surat-perintah-penahanan", tags=['surat-perintah-penahanan'])


@router.post("/create-surat", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_surat_perintah_penahanan(surat_perintah: SuratPerintahPenahananBase, db: Session = Depends(get_db)):
    db_narapidana = db.query(Narapidana).filter(Narapidana.nomor_narapidana == surat_perintah.nomor_narapidana).first()
    if db_narapidana is None:
        raise HTTPException(status_code=404, detail='Narapidana Tidak Ditemukan!')

    db_surat_perintah = SuratPerintahPenahanan(**surat_perintah.dict())
    db.add(db_surat_perintah)
    db.commit()
    return {'detail': 'RESULT_OK'}


# Read all
@router.get("/get-surat", dependencies=[Depends(get_current_user)])
async def get_all_surat_perintah_penahanan(db: Session = Depends(get_db)):
    return db.query(SuratPerintahPenahanan).all()


# Read
@router.get("/get-surat/{nomor_surat}", dependencies=[Depends(get_current_user)])
async def get_surat_perintah_penahanan(nomor_surat: str, db: Session = Depends(get_db)):
    surat_perintah = db.query(SuratPerintahPenahanan).filter(SuratPerintahPenahanan.nomor_surat == nomor_surat).first()
    if surat_perintah is None:
        raise HTTPException(status_code=404, detail='Surat Perintah Penahanan Tidak Ditemukan!')
    return surat_perintah

@router.get("/get-surat-narapidana/{nomor_narapidana}", dependencies=[Depends(get_current_user)])
async def get_surat_perintah_penahanan_narapidana(nomor_narapidana: str, db: Session = Depends(get_db)):
    surat_perintah = db.query(SuratPerintahPenahanan).filter(SuratPerintahPenahanan.nomor_narapidana == nomor_narapidana).first()
    if surat_perintah is None:
        return "Tidak Ditemukan!"
    return surat_perintah


# Update
@router.put("/update-surat/{nomor_surat}", dependencies=[Depends(get_current_user)])
async def update_surat_perintah_penahanan(nomor_surat: str, surat_perintah: SuratPerintahPenahananBase,
                                          db: Session = Depends(get_db)):
    db_surat_perintah = db.query(SuratPerintahPenahanan).filter(
        SuratPerintahPenahanan.nomor_surat == nomor_surat).first()


    db_surat_perintah.tanggal_penerbitan = surat_perintah.tanggal_penerbitan
    db_surat_perintah.keterangan = surat_perintah.keterangan
    db_surat_perintah.nomor_narapidana = surat_perintah.nomor_narapidana
    db.commit()
    return {'detail': 'RESULT_OK'}


# Delete
@router.delete("/delete-surat/{nomor_surat}", dependencies=[Depends(get_current_user)])
async def delete_surat_perintah_penahanan(nomor_surat: str, db: Session = Depends(get_db)):
    db_surat_perintah = db.query(SuratPerintahPenahanan).filter(
        SuratPerintahPenahanan.nomor_surat == nomor_surat).first()
    if db_surat_perintah is None:
        raise HTTPException(status_code=404, detail="Surat Perintah Penahanan tidak ditemukan!")
    db.delete(db_surat_perintah)
    db.commit()
    return {"detail": 'RESULT_OK'}
