from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class RoleEnum(str, Enum):
    admin = 'admin'
    staff_lapas = 'staff lapas'

class PenggunaBase(BaseModel):
    nomor_kepegawaian: str
    nama: str
    password: str
    role: RoleEnum

class PenggunaBaseEdit(BaseModel):
    nomor_kepegawaian: str
    nama: str


class NarapidanaBase(BaseModel):
    nomor_narapidana: str
    nama: str
    tanggal_masuk: date
    tanggal_lahir: date
    deskripsi_kasus: str
    nomor_kamar: str


class IzinKunjunganBase(BaseModel):
    nomor_izin: str
    waktu_kunjungan: datetime
    keterangan: str
    penanggung_jawab: str
    nomor_narapidana: str


class KegiatanHarianBase(BaseModel):
    nomor_kegiatan: str
    tanggal_kegiatan: date
    deskripsi_kegiatan: str
    lokasi: str
    penanggung_jawab: str


class SuratPerintahPenahananBase(BaseModel):
    nomor_surat: str
    tanggal_penerbitan: date
    keterangan: str
    nomor_narapidana: str


class PengunjungBase(BaseModel):
    id_pengunjung:int
    nama_pengunjung: str
    nomor_izin: str


class Token(BaseModel):
    Authorization :str
    detail:str


class TokenData(BaseModel):
    nomor_kepegawaian: str
    password: str


class OAuth2PasswordRequestFormCustom(BaseModel):
    nomor_kepegawaian: str
    password: str
