-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: quan_li_ban_quan_ao
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Tạo database nếu chưa có
CREATE DATABASE IF NOT EXISTS quanly_banhang CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE quanly_banhang;

-- Bảng khách hàng
CREATE TABLE khach_hang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten VARCHAR(100) NOT NULL,
    sdt VARCHAR(20),
    dia_chi VARCHAR(255),
    email VARCHAR(100),
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bảng nhân viên
CREATE TABLE nhan_vien (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten VARCHAR(100) NOT NULL,
    sdt VARCHAR(20),
    dia_chi VARCHAR(255),
    email VARCHAR(100),
    chuc_vu VARCHAR(50),
    ngay_vao_lam DATE
);

-- Bảng sản phẩm
CREATE TABLE san_pham (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten VARCHAR(100) NOT NULL,
    loai VARCHAR(50),
    gia_nhap DECIMAL(15,2),
    gia_ban DECIMAL(15,2),
    so_luong INT DEFAULT 0,
    don_vi_tinh VARCHAR(20),
    mo_ta TEXT
);

-- Bảng hóa đơn
CREATE TABLE hoa_don (
    id INT AUTO_INCREMENT PRIMARY KEY,
    khach_hang_id INT,
    nhan_vien_id INT,
    ngay_lap DATETIME DEFAULT CURRENT_TIMESTAMP,
    tong_tien DECIMAL(15,2),
    FOREIGN KEY (khach_hang_id) REFERENCES khach_hang(id),
    FOREIGN KEY (nhan_vien_id) REFERENCES nhan_vien(id)
);

-- Bảng chi tiết hóa đơn
CREATE TABLE chi_tiet_hoa_don (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hoa_don_id INT,
    san_pham_id INT,
    so_luong INT,
    don_gia DECIMAL(15,2),
    thanh_tien DECIMAL(15,2),
    FOREIGN KEY (hoa_don_id) REFERENCES hoa_don(id),
    FOREIGN KEY (san_pham_id) REFERENCES san_pham(id)
);

-- Bảng phiếu hàng (nhập/xuất kho)
CREATE TABLE phieu_hang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loai ENUM('nhap','xuat') NOT NULL,
    ngay_lap DATETIME DEFAULT CURRENT_TIMESTAMP,
    nhan_vien_id INT,
    ghi_chu TEXT,
    FOREIGN KEY (nhan_vien_id) REFERENCES nhan_vien(id)
);

-- Bảng chi tiết phiếu hàng
CREATE TABLE chi_tiet_phieu_hang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phieu_hang_id INT,
    san_pham_id INT,
    so_luong INT,
    don_gia DECIMAL(15,2),
    FOREIGN KEY (phieu_hang_id) REFERENCES phieu_hang(id),
    FOREIGN KEY (san_pham_id) REFERENCES san_pham(id)
);

--
-- Table structure for table `danh_muc_san_pham`
--

DROP TABLE IF EXISTS `danh_muc_san_pham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_muc_san_pham` (
  `id_danh_muc` int NOT NULL,
  `ten_danh_muc` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_danh_muc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_muc_san_pham`
--

LOCK TABLES `danh_muc_san_pham` WRITE;
/*!40000 ALTER TABLE `danh_muc_san_pham` DISABLE KEYS */;
INSERT INTO `danh_muc_san_pham` VALUES (1,'Ao'),(2,'Quan'),(3,'Giay'),(4,'Dep'),(5,'Non');
/*!40000 ALTER TABLE `danh_muc_san_pham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_sach_khach_hang`
--

DROP TABLE IF EXISTS `danh_sach_khach_hang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_khach_hang` (
  `id_khach_hang` int NOT NULL,
  `ten_khach_hang` varchar(45) DEFAULT NULL,
  `tuoi_khach_hang` int DEFAULT NULL,
  `gioi_tinh_khach_hang` varchar(45) DEFAULT NULL,
  `dia_chi_khach_hang` varchar(45) DEFAULT NULL,
  `so_dien_thoai` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_khach_hang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_khach_hang`
--

LOCK TABLES `danh_sach_khach_hang` WRITE;
/*!40000 ALTER TABLE `danh_sach_khach_hang` DISABLE KEYS */;
INSERT INTO `danh_sach_khach_hang` VALUES (0,'aa',1,'nam','A','111111'),(1,'bb',2,'nu','B','222222'),(2,'cc',3,'nam','A','32313213'),(3,'dd',4,'nam','C','41224'),(4,'ee',5,'nu','D','21324214'),(5,'ff',6,'nu','D','124'),(6,'gg',7,'nu','C','346346'),(7,'hh',8,'nam','A','123'),(8,'a',3,'n','B','977'),(9,'a',1,'nn','A','543'),(11,'â',56,'n','BA','1'),(12,'â',67,'n','A','1'),(13,'a',56,'n','BA','1'),(14,'a',9,'n','A','1'),(15,'b',6,'n','B','1'),(16,'ád',89,'n','A','1'),(17,'sf',7,'n','B','1'),(18,'a',6,'n','A','1'),(19,'a',5,'n','B','1'),(20,'a',11,'n','A','1'),(21,'ae',22,'n','C','1'),(111,'new001',NULL,NULL,'new001','new001'),(123,'new002',26,'nam','AA','0909090909'),(3636,'ba sau',36,'nam','Thanh Hoa','0363636363636');
/*!40000 ALTER TABLE `danh_sach_khach_hang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_sach_nhan_vien`
--

DROP TABLE IF EXISTS `danh_sach_nhan_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_nhan_vien` (
  `id_nhan_vien` int NOT NULL,
  `ten_nhan_vien` varchar(45) DEFAULT NULL,
  `tuoi_nhan_vien` int DEFAULT NULL,
  `gioi_tinh_nhan_vien` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_nhan_vien`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_nhan_vien`
--

LOCK TABLES `danh_sach_nhan_vien` WRITE;
/*!40000 ALTER TABLE `danh_sach_nhan_vien` DISABLE KEYS */;
INSERT INTO `danh_sach_nhan_vien` VALUES (0,'a',11,'nam'),(1,'b',22,'nam'),(2,'c',33,'nam'),(3,'d',44,'nu'),(4,'e',55,'nu'),(5,'f',66,'nu'),(6,'g',77,'nam');
/*!40000 ALTER TABLE `danh_sach_nhan_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_sach_san_pham`
--

DROP TABLE IF EXISTS `danh_sach_san_pham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_san_pham` (
  `id_san_pham` int NOT NULL AUTO_INCREMENT,
  `ten_san_pham` varchar(50) NOT NULL,
  `id_danh_muc` int DEFAULT NULL,
  `gia_san_pham` int DEFAULT NULL,
  `so_luong_ton_kho` int DEFAULT NULL,
  `mo_ta_san_pham` varchar(45) DEFAULT NULL,
  `gia_nhap_san_pham` int DEFAULT NULL,
  PRIMARY KEY (`id_san_pham`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_san_pham`
--

LOCK TABLES `danh_sach_san_pham` WRITE;
/*!40000 ALTER TABLE `danh_sach_san_pham` DISABLE KEYS */;
INSERT INTO `danh_sach_san_pham` VALUES (1,'a',1,11,10,'a',1),(2,'coin card',2,100000,500,'coin card',50000),(3,'card coin',3,200000,500,'card coin',100000),(4,'d',1,44,10,'d',1),(5,'san pham moi',5,555555,555,'555555',555),(6,'f',1,66,20,'f',1),(7,'q',1,77,30,'g',1),(8,'ewq',1,88,40,'h',1),(9,'qưe',1,99,20,'j ',1),(10,'qưe',1,0,30,'k',1),(11,'ret',1,1221,10,'l',1),(12,'dfg',1,1331,30,'k',1),(13,'qưe',1,1441,20,'l',1),(14,'ỵt',1,1551,40,'m',1),(15,'ads',1,1661,50,'n',1),(16,'bnf',1,333,90,'o',1),(17,'klk',1,333,100,'p',1),(18,'ôp',1,444,25,'q',1),(19,'iuei',1,555,40,'r',1),(20,'poep',1,666,60,'s',1),(21,'uqye',1,777,80,'t',1),(22,'qiwue',1,888,90,'w',1);
/*!40000 ALTER TABLE `danh_sach_san_pham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lich_su_hoa_don`
--

DROP TABLE IF EXISTS `lich_su_hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lich_su_hoa_don` (
  `id_hoa_don` int NOT NULL,
  `tong_gia_tri_hoa_don` int DEFAULT NULL,
  `id_khach_hang` int DEFAULT NULL,
  `id_nhan_vien` int DEFAULT NULL,
  `loai_hoa_don` varchar(45) DEFAULT NULL,
  `ngay_giao_dich` date DEFAULT NULL,
  PRIMARY KEY (`id_hoa_don`),
  UNIQUE KEY `id_hoa_don_UNIQUE` (`id_hoa_don`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_su_hoa_don`
--

LOCK TABLES `lich_su_hoa_don` WRITE;
/*!40000 ALTER TABLE `lich_su_hoa_don` DISABLE KEYS */;
INSERT INTO `lich_su_hoa_don` VALUES (0,100,4,NULL,'B','2025-01-03'),(1,200,3,NULL,'B','2025-01-04'),(2,300,2,NULL,'B','2025-01-04'),(3,400,1,NULL,'B','2025-02-01'),(4,500,999999,NULL,'M','2025-02-01'),(5,100,999999,NULL,'M','2025-03-01'),(6,300,999999,NULL,'M','2025-03-25'),(7,100,1,NULL,'B','2025-04-02'),(8,300,999999,NULL,'M','2025-04-03'),(9,200,2,NULL,'B','2025-05-01'),(10,100,1,NULL,'B','2025-05-25'),(11,11,1,NULL,'B','2025-04-20'),(12,500,5,NULL,'B','2025-01-01'),(13,11,0,NULL,'B','2025-04-20'),(14,11,0,NULL,'B','2025-04-20'),(15,11,0,NULL,'B','2025-04-20'),(16,11,22,NULL,'B','2025-04-20'),(17,11,2,NULL,'B','2025-04-20'),(18,11,0,NULL,'B','2025-04-20'),(19,11,1,NULL,'B','2025-04-20'),(20,11,1,NULL,'B','2025-04-20'),(21,99,1,NULL,'B','2025-04-20'),(22,99,12,NULL,'B','2025-04-20'),(23,110,5,NULL,'B','2025-04-21'),(24,4389,3,NULL,'B','2025-04-21'),(25,2717,1,NULL,'B','2025-04-23'),(26,500275,5,NULL,'B','2025-04-23');
/*!40000 ALTER TABLE `lich_su_hoa_don` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 15:44:07
