-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 02, 2024 at 01:21 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_penjara`
--

-- --------------------------------------------------------

--
-- Table structure for table `izin_kunjungan`
--

CREATE TABLE `izin_kunjungan` (
  `nomor_izin` char(12) NOT NULL,
  `waktu_kunjungan` datetime DEFAULT current_timestamp(),
  `keterangan` text DEFAULT NULL,
  `penanggung_jawab` char(12) DEFAULT NULL,
  `nomor_narapidana` char(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `izin_kunjungan`
--

INSERT INTO `izin_kunjungan` (`nomor_izin`, `waktu_kunjungan`, `keterangan`, `penanggung_jawab`, `nomor_narapidana`) VALUES
('1', '2024-07-10 06:54:00', 'Aman Terkendali', 'H071221075', 'LP-4');

-- --------------------------------------------------------

--
-- Table structure for table `kegiatan_harian`
--

CREATE TABLE `kegiatan_harian` (
  `nomor_kegiatan` char(12) NOT NULL,
  `tanggal_kegiatan` date DEFAULT curdate(),
  `deskripsi_kegiatan` text DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `penanggung_jawab` char(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kegiatan_harian`
--

INSERT INTO `kegiatan_harian` (`nomor_kegiatan`, `tanggal_kegiatan`, `deskripsi_kegiatan`, `lokasi`, `penanggung_jawab`) VALUES
('1', '2024-07-09', 'Makan Bersama', 'Kantin', 'H071221079');

-- --------------------------------------------------------

--
-- Table structure for table `narapidana`
--

CREATE TABLE `narapidana` (
  `nomor_narapidana` char(12) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `tanggal_masuk` date DEFAULT curdate(),
  `tanggal_lahir` date DEFAULT NULL,
  `deskripsi_kasus` text DEFAULT NULL,
  `nomor_kamar` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `narapidana`
--

INSERT INTO `narapidana` (`nomor_narapidana`, `nama`, `tanggal_masuk`, `tanggal_lahir`, `deskripsi_kasus`, `nomor_kamar`) VALUES
('LP-4', 'Mario', '2024-07-11', '2007-07-01', 'Pencucian uang', 'VVIP-3'),
('LP-5', 'Mario', '2024-07-19', '2007-07-01', 'e', 'ssd');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `nomor_kepegawaian` char(12) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','staff lapas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`nomor_kepegawaian`, `nama`, `password`, `role`) VALUES
('H071221075', 'Mario Valerian', '$2b$12$a6/5ROqjvk.IuuVBPaurY.YYIJPVH9r1T8lr9Pz8MiBp4rZI5IZwy', 'staff lapas'),
('H071221079', 'Mario Valerian Rante Ta\'dung', '$2b$12$u956YmmollmsR4ufsaX/TOkRKwofb4jU.6YA7Lj9gxrN9KItJ5..2', 'staff lapas'),
('SUPERUSER', 'SUPERUSER', '$2b$12$a6/5ROqjvk.IuuVBPaurY.YYIJPVH9r1T8lr9Pz8MiBp4rZI5IZwy', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `pengunjung`
--

CREATE TABLE `pengunjung` (
  `id_pengunjung` int(11) NOT NULL,
  `nama_pengunjung` varchar(100) NOT NULL,
  `nomor_izin` char(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengunjung`
--

INSERT INTO `pengunjung` (`id_pengunjung`, `nama_pengunjung`, `nomor_izin`) VALUES
(1, 'Mario Valerian', '1');

-- --------------------------------------------------------

--
-- Table structure for table `surat_perintah_penahanan`
--

CREATE TABLE `surat_perintah_penahanan` (
  `nomor_surat` char(16) NOT NULL,
  `tanggal_penerbitan` date DEFAULT NULL,
  `keterangan` text DEFAULT NULL,
  `nomor_narapidana` char(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `surat_perintah_penahanan`
--

INSERT INTO `surat_perintah_penahanan` (`nomor_surat`, `tanggal_penerbitan`, `keterangan`, `nomor_narapidana`) VALUES
('OP01', '2024-07-16', 'd', 'LP-5'),
('OP03', '2024-07-03', 'Aaman3 y', 'LP-4');

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist`
--

CREATE TABLE `token_blacklist` (
  `id` int(11) NOT NULL,
  `token` varchar(512) NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `izin_kunjungan`
--
ALTER TABLE `izin_kunjungan`
  ADD PRIMARY KEY (`nomor_izin`),
  ADD KEY `penanggung_jawab` (`penanggung_jawab`),
  ADD KEY `nomor_narapidana` (`nomor_narapidana`);

--
-- Indexes for table `kegiatan_harian`
--
ALTER TABLE `kegiatan_harian`
  ADD PRIMARY KEY (`nomor_kegiatan`),
  ADD KEY `penanggung_jawab` (`penanggung_jawab`);

--
-- Indexes for table `narapidana`
--
ALTER TABLE `narapidana`
  ADD PRIMARY KEY (`nomor_narapidana`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`nomor_kepegawaian`);

--
-- Indexes for table `pengunjung`
--
ALTER TABLE `pengunjung`
  ADD PRIMARY KEY (`id_pengunjung`),
  ADD KEY `fk_pengunjung_izin` (`nomor_izin`);

--
-- Indexes for table `surat_perintah_penahanan`
--
ALTER TABLE `surat_perintah_penahanan`
  ADD PRIMARY KEY (`nomor_surat`),
  ADD KEY `nomor_narapidana` (`nomor_narapidana`);

--
-- Indexes for table `token_blacklist`
--
ALTER TABLE `token_blacklist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_token_blacklist_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pengunjung`
--
ALTER TABLE `pengunjung`
  MODIFY `id_pengunjung` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `token_blacklist`
--
ALTER TABLE `token_blacklist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `izin_kunjungan`
--
ALTER TABLE `izin_kunjungan`
  ADD CONSTRAINT `izin_kunjungan_ibfk_1` FOREIGN KEY (`penanggung_jawab`) REFERENCES `pengguna` (`nomor_kepegawaian`),
  ADD CONSTRAINT `izin_kunjungan_ibfk_2` FOREIGN KEY (`nomor_narapidana`) REFERENCES `narapidana` (`nomor_narapidana`) ON DELETE CASCADE;

--
-- Constraints for table `kegiatan_harian`
--
ALTER TABLE `kegiatan_harian`
  ADD CONSTRAINT `kegiatan_harian_ibfk_1` FOREIGN KEY (`penanggung_jawab`) REFERENCES `pengguna` (`nomor_kepegawaian`);

--
-- Constraints for table `pengunjung`
--
ALTER TABLE `pengunjung`
  ADD CONSTRAINT `fk_pengunjung_izin` FOREIGN KEY (`nomor_izin`) REFERENCES `izin_kunjungan` (`nomor_izin`) ON DELETE CASCADE;

--
-- Constraints for table `surat_perintah_penahanan`
--
ALTER TABLE `surat_perintah_penahanan`
  ADD CONSTRAINT `surat_perintah_penahanan_ibfk_1` FOREIGN KEY (`nomor_narapidana`) REFERENCES `narapidana` (`nomor_narapidana`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
