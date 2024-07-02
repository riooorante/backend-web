from datetime import datetime, date

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Date, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from app.schemas import RoleEnum

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/db_penjara"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Narapidana(Base):
    __tablename__ = 'narapidana'
    nomor_narapidana = Column(String(12), primary_key=True)
    nama = Column(String(255))
    tanggal_masuk = Column(Date, default=date.today)
    tanggal_lahir = Column(Date)
    deskripsi_kasus = Column(Text)
    nomor_kamar = Column(String(10))


class Pengguna(Base):
    __tablename__ = 'pengguna'

    nomor_kepegawaian = Column(String(12), primary_key=True)
    nama = Column(String(100))
    password = Column(String(255))
    role = Column(Enum('admin', 'staff lapas', name='role_enum'))


class IzinKunjungan(Base):
    __tablename__ = 'izin_kunjungan'
    nomor_izin = Column(String(12), primary_key=True)
    waktu_kunjungan = Column(DateTime, default=datetime.now)
    keterangan = Column(Text)
    penanggung_jawab = Column(String(12), ForeignKey('pengguna.nomor_kepegawaian'))
    nomor_narapidana = Column(String(12), ForeignKey('narapidana.nomor_narapidana'))
    pengguna = relationship("Pengguna")


class KegiatanHarian(Base):
    __tablename__ = 'kegiatan_harian'
    nomor_kegiatan = Column(String(12), primary_key=True)
    tanggal_kegiatan = Column(Date, default=date.today)
    deskripsi_kegiatan = Column(Text)
    lokasi = Column(String(100))
    penanggung_jawab = Column(String(12), ForeignKey('pengguna.nomor_kepegawaian'))
    pengguna = relationship("Pengguna")


class SuratPerintahPenahanan(Base):
    __tablename__ = 'surat_perintah_penahanan'
    nomor_surat = Column(String(16), primary_key=True)
    tanggal_penerbitan = Column(Date)
    keterangan = Column(Text)
    nomor_narapidana = Column(String(12), ForeignKey('narapidana.nomor_narapidana'))
    narapidana = relationship("Narapidana")


class Pengunjung(Base):
    __tablename__ = 'pengunjung'

    id_pengunjung = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_pengunjung = Column(String(100), nullable=False)
    nomor_izin = Column(String(12), ForeignKey('izin_kunjungan.nomor_izin'), nullable=False)
    izin_kunjungan = relationship("IzinKunjungan")


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), nullable=False)
    created_at = Column(DateTime, nullable=False)