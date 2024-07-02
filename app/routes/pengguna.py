import logging
from typing import List, Dict

from app.auth import hash_password, get_current_user
from app.config import get_db
from app.models import Pengguna
from app.schemas import PenggunaBase, PenggunaBaseEdit
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pengguna", tags=['pengguna'])

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@router.post("/create-pengguna", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str],
             dependencies=[Depends(get_current_user)])
async def create_pengguna(pengguna: PenggunaBase, db: Session = Depends(get_db)):
    try:
        pengguna_pass = pengguna.password

        pengguna.password = hash_password(pengguna_pass)
        db_pengguna = Pengguna(**pengguna.dict())
        db.add(db_pengguna)
        db.commit()
        db.refresh(db_pengguna)
        return {'detail': 'RESULT_OK'}
    except SQLAlchemyError as e:
        logger.error(f"Error creating Pengguna: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Gagal Menambahkan Pengguna Baru! Error: {str(e)}')
    finally:
        db.close()


@router.get("/get-pengguna", response_model=List[PenggunaBase], dependencies=[Depends(get_current_user)])
async def get_all_pengguna(db: Session = Depends(get_db)):
    try:
        pengguna_list = db.query(Pengguna).all()
        return pengguna_list
    except SQLAlchemyError as e:
        logger.error(f"Error fetching Pengguna list: {e}")
        raise HTTPException(status_code=500, detail='Gagal Mengambil Daftar Pengguna')


@router.get("/get-pengguna/{nomor_kepegawaian}", response_model=PenggunaBase, dependencies=[Depends(get_current_user)])
async def get_pengguna(nomor_kepegawaian: str, db: Session = Depends(get_db)):
    try:
        pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == nomor_kepegawaian).first()
        if not pengguna:
            raise HTTPException(status_code=404, detail='Pengguna Tidak Ditemukan!')
        return pengguna
    except SQLAlchemyError as e:
        logger.error(f"Error fetching Pengguna with nomor_kepegawaian {nomor_kepegawaian}: {e}")
        raise HTTPException(status_code=500, detail='Gagal Mengambil Data Pengguna')


@router.put("/update-pengguna/{nomor_kepegawaian}", response_model=Dict[str, str],
            dependencies=[Depends(get_current_user)])
async def update_pengguna(nomor_kepegawaian: str, pengguna: PenggunaBaseEdit, db: Session = Depends(get_db)):
    try:
        db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == nomor_kepegawaian).first()
        if not db_pengguna:
            raise HTTPException(status_code=404, detail='Pengguna Tidak Ditemukan!')

        db_pengguna.nama = pengguna.nama
        db.commit()
        return {'detail': 'RESULT_OK'}
    except SQLAlchemyError as e:
        logger.error(f"Error updating Pengguna with nomor_kepegawaian {nomor_kepegawaian}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Gagal Memperbarui Pengguna! Error: {str(e)}')
    finally:
        db.close()


@router.delete("/delete-pengguna/{nomor_kepegawaian}", response_model=Dict[str, str],
               dependencies=[Depends(get_current_user)])
async def delete_pengguna(nomor_kepegawaian: str, db: Session = Depends(get_db)):
    try:
        db_pengguna = db.query(Pengguna).filter(Pengguna.nomor_kepegawaian == nomor_kepegawaian).first()
        if not db_pengguna:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan!")
        nama_pengguna = db_pengguna.nama
        db.delete(db_pengguna)
        db.commit()
        return {"detail": 'RESULT_OK'}
    except SQLAlchemyError as e:
        logger.error(f"Error deleting Pengguna with nomor_kepegawaian {nomor_kepegawaian}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Gagal Menghapus Pengguna! Error: {str(e)}')
    finally:
        db.close()
