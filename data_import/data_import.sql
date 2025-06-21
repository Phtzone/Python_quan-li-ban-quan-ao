CREATE DATABASE  IF NOT EXISTS `quan_li_ban_quan_ao` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `quan_li_ban_quan_ao`;
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

--
-- Table structure for table `chi_tiet_hoa_don`
--

DROP TABLE IF EXISTS `chi_tiet_hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_hoa_don` (
  `id_chi_tiet` int NOT NULL AUTO_INCREMENT,
  `id_hoa_don` int DEFAULT NULL,
  `id_san_pham` int DEFAULT NULL,
  `so_luong` int DEFAULT NULL,
  PRIMARY KEY (`id_chi_tiet`),
  KEY `id_hoa_don_idx` (`id_hoa_don`),
  KEY `id_san_pham_idx` (`id_san_pham`),
  CONSTRAINT `id_hoa_don` FOREIGN KEY (`id_hoa_don`) REFERENCES `lich_su_hoa_don` (`id_hoa_don`),
  CONSTRAINT `id_san_pham` FOREIGN KEY (`id_san_pham`) REFERENCES `danh_sach_san_pham` (`id_san_pham`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_hoa_don`
--

LOCK TABLES `chi_tiet_hoa_don` WRITE;
/*!40000 ALTER TABLE `chi_tiet_hoa_don` DISABLE KEYS */;
INSERT INTO `chi_tiet_hoa_don` VALUES (62,1,1,50),(63,2,1,50),(64,3,2,30),(65,4,1,5),(66,4,2,5),(67,5,1,10),(68,6,3,30),(69,7,4,60),(70,8,5,70),(71,9,6,20),(72,10,7,30),(73,11,8,90),(74,12,9,80),(75,13,10,55),(76,14,11,70),(77,15,12,67),(78,16,13,90),(79,17,14,20),(80,18,15,100),(81,19,9,1),(82,19,8,1),(83,19,7,1),(84,19,10,1),(85,20,9,2),(86,20,8,1),(87,20,7,2),(88,20,10,1),(89,20,5,4),(90,21,16,50),(91,22,4,10),(92,22,15,10);
/*!40000 ALTER TABLE `chi_tiet_hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `danh_sach_khach_hang` VALUES (0,'Cửa Hàng',999,'siu','Cửa Hàng','7777777'),(1,'Đặng Thị Nam',39,'Nam','Quận Hoàn Kiếm, Hà Nội','321798548'),(2,'Phạm Gia Linh',35,'Nữ','Quận 1, TP.HCM','502074554'),(3,'Trần Thị Linh',57,'Nam','Quận Hoàn Kiếm, Hà Nội','218010251'),(4,'Nguyễn Quốc Trang',54,'Nữ','Huyện Hóc Môn, TP.HCM','725145611'),(5,'Phạm Thanh Dũng',42,'Nữ','Thành phố Biên Hòa, Đồng Nai','447358122'),(6,'Bùi Hữu Huy',45,'Nữ','Huyện Hóc Môn, TP.HCM','213401970'),(7,'Đặng Thành Đạt',58,'Nữ','Quận Đống Đa, Hà Nội','594819958'),(8,'Phạm Minh Sơn',57,'Nữ','Quận Long Biên, Hà Nội','825304138'),(9,'Hoàng Văn Quang',59,'Nữ','Quận Đống Đa, Hà Nội','615380246'),(10,'Đặng Văn Tú',18,'Nam','Quận 10, TP.HCM','548221761'),(11,'Hoàng Quốc An',38,'Nam','Thành phố Biên Hòa, Đồng Nai','915043734'),(12,'Bùi Văn An',26,'Nam','Quận Ninh Kiều, Cần Thơ','481405648'),(13,'Nguyễn Xuân Khánh',54,'Nữ','Quận Bình Thạnh, TP.HCM','203043544'),(14,'Hoàng Gia Đạt',59,'Nữ','Quận 3, TP.HCM','661021083'),(15,'Lê Xuân An',20,'Nam','Quận 10, TP.HCM','308210576'),(16,'Đặng Xuân Bình',23,'Nữ','Quận Ninh Kiều, Cần Thơ','851148214'),(17,'Phạm Thanh Phúc',48,'Nữ','Huyện Long Thành, Đồng Nai','706025687'),(18,'Đặng Minh An',43,'Nam','Quận Đống Đa, Hà Nội','914785634'),(19,'Huỳnh Xuân Nam',42,'Nam','Quận Hoàn Kiếm, Hà Nội','972429595'),(20,'Huỳnh Quốc Thảo',28,'Nam','Quận Bình Thạnh, TP.HCM','566494549'),(21,'Phan Quốc Quang',55,'Nữ','Quận 3, TP.HCM','201006570'),(22,'Bùi Quốc Trang',31,'Nam','Quận Thanh Khê, Đà Nẵng','430283252'),(23,'Phạm Ngọc Cường',33,'Nữ','Quận Hoàn Kiếm, Hà Nội','587882505'),(24,'Đặng Văn Dũng',33,'Nữ','Quận 7, TP.HCM','925406636'),(25,'Hoàng Văn Thảo',55,'Nữ','Quận Đống Đa, Hà Nội','123766829'),(26,'Hoàng Hữu Tú',55,'Nam','Quận 3, TP.HCM','412323503'),(27,'Phan Hữu Bình',23,'Nam','Quận Thanh Khê, Đà Nẵng','738294858'),(28,'Đặng Xuân Cường',28,'Nam','Quận Gò Vấp, TP.HCM','766855296'),(29,'Bùi Gia Trang',29,'Nữ','Quận 10, TP.HCM','257423162'),(30,'Huỳnh Thành Phúc',46,'Nam','Quận 1, TP.HCM','755040963'),(31,'Lê Thị Bình',44,'Nam','Quận Thanh Xuân, Hà Nội','446497848'),(32,'Trần Quốc Trang',46,'Nam','Quận Thanh Xuân, Hà Nội','826273813'),(33,'Huỳnh Thanh Linh',41,'Nữ','Quận Hải Châu, Đà Nẵng','381525429'),(34,'Hoàng Thanh Trang',57,'Nam','Quận 1, TP.HCM','651988574'),(35,'Huỳnh Ngọc Trang',45,'Nam','Quận 5, TP.HCM','106856707'),(36,'Võ Gia Tú',39,'Nam','Quận Hoàn Kiếm, Hà Nội','295007303'),(37,'Trần Quốc Bình',35,'Nam','Quận Thanh Khê, Đà Nẵng','747020733'),(38,'Nguyễn Xuân Khánh',60,'Nữ','Quận Đống Đa, Hà Nội','183703852'),(39,'Võ Gia Quang',60,'Nam','Huyện Hóc Môn, TP.HCM','535871782'),(40,'Nguyễn Thanh An',43,'Nữ','Quận 1, TP.HCM','805293942'),(41,'Phạm Thành An',35,'Nam','Quận 5, TP.HCM','990128255'),(42,'Phạm Thị Quang',35,'Nữ','Quận Bình Thủy, Cần Thơ','876266957'),(43,'Phan Minh Trang',40,'Nữ','Quận 5, TP.HCM','920172523'),(44,'Lê Hữu Mai',31,'Nữ','Quận Đống Đa, Hà Nội','475906822'),(45,'Lê Thị Trang',25,'Nữ','Quận Hoàn Kiếm, Hà Nội','100445193'),(46,'Võ Ngọc Bình',40,'Nam','Quận Thanh Khê, Đà Nẵng','613023931'),(47,'Huỳnh Ngọc Phúc',30,'Nữ','Quận Bình Thạnh, TP.HCM','803467315'),(48,'Bùi Minh Phúc',37,'Nữ','Quận Bình Thạnh, TP.HCM','943810333'),(49,'Trần Văn Bình',40,'Nam','Quận 1, TP.HCM','745695152'),(50,'Đặng Quốc Cường',37,'Nữ','Huyện Hóc Môn, TP.HCM','190365869'),(51,'Hoàng Ngọc Huy',26,'Nam','Huyện Long Thành, Đồng Nai','149275018'),(52,'Lê Thanh Sơn',35,'Nam','Quận Bình Thạnh, TP.HCM','671359112'),(53,'Võ Thị Sơn',20,'Nữ','Quận Long Biên, Hà Nội','523422341'),(54,'Võ Xuân Dũng',25,'Nữ','Quận Cầu Giấy, Hà Nội','979155385'),(55,'Phan Minh Thảo',43,'Nam','Quận 5, TP.HCM','874970354'),(56,'Phạm Gia Trang',35,'Nam','Quận 1, TP.HCM','797492343'),(57,'Đặng Thị Sơn',34,'Nam','Huyện Long Thành, Đồng Nai','962200636'),(58,'Phạm Văn Tú',42,'Nam','Quận Bình Thủy, Cần Thơ','418671920'),(59,'Nguyễn Quốc Nam',19,'Nam','Quận Long Biên, Hà Nội','417415828'),(60,'Đặng Thanh Linh',34,'Nữ','Quận Ninh Kiều, Cần Thơ','420010177'),(61,'Võ Xuân An',60,'Nữ','Quận Đống Đa, Hà Nội','902820529'),(62,'Võ Văn Nam',60,'Nam','Quận 1, TP.HCM','397854842'),(63,'Lê Xuân Dũng',37,'Nam','Quận Bình Thủy, Cần Thơ','729725877'),(64,'Hoàng Xuân Huy',23,'Nữ','Huyện Long Thành, Đồng Nai','156378532'),(65,'Đặng Thanh Huy',56,'Nữ','Quận 3, TP.HCM','971531216'),(66,'Lê Hữu Linh',32,'Nữ','Quận Gò Vấp, TP.HCM','426087861'),(67,'Phạm Thị Sơn',19,'Nữ','Quận Cầu Giấy, Hà Nội','773215145'),(68,'Hoàng Quốc Nam',23,'Nam','Quận 1, TP.HCM','385436293'),(69,'Trần Thị Quang',20,'Nữ','Huyện Long Thành, Đồng Nai','590048470'),(70,'Đặng Thị Mai',54,'Nữ','Quận Cầu Giấy, Hà Nội','698922987'),(71,'Đặng Quốc Nam',24,'Nữ','Quận 7, TP.HCM','769219791'),(72,'Võ Hữu Dũng',48,'Nam','Quận Gò Vấp, TP.HCM','139435504'),(73,'Võ Văn Sơn',55,'Nữ','Quận Gò Vấp, TP.HCM','939588397'),(74,'Hoàng Thị Dũng',21,'Nam','Quận Cầu Giấy, Hà Nội','634358577'),(75,'Phạm Văn Quang',56,'Nữ','Huyện Long Thành, Đồng Nai','944562727'),(76,'Hoàng Gia Thảo',58,'Nữ','Quận 1, TP.HCM','876269302'),(77,'Phan Thanh Nam',26,'Nữ','Quận Hoàn Kiếm, Hà Nội','899322307'),(78,'Võ Hữu Thảo',33,'Nam','Quận Gò Vấp, TP.HCM','551027461'),(79,'Phan Hữu Cường',57,'Nam','Quận Thanh Khê, Đà Nẵng','101343227'),(80,'Võ Xuân Đạt',40,'Nam','Quận 7, TP.HCM','525182897'),(81,'Lê Hữu Dũng',60,'Nữ','Quận 1, TP.HCM','217541598'),(82,'Bùi Thị Quang',52,'Nam','Huyện Long Thành, Đồng Nai','658913185'),(83,'Hoàng Thanh Huy',51,'Nữ','Huyện Hóc Môn, TP.HCM','425038163'),(84,'Chôn Ni Đặng',77,'Nam','Quận 1, TP.HCM','07070707070'),(85,'Xê Rờ Bảy',77,'Nữ','Quận 7, TP.HCM','7777777777');
/*!40000 ALTER TABLE `danh_sach_khach_hang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_sach_san_pham`
--

DROP TABLE IF EXISTS `danh_sach_san_pham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danh_sach_san_pham` (
  `id_san_pham` int NOT NULL AUTO_INCREMENT,
  `ten_san_pham` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_vi_0900_ai_ci NOT NULL,
  `id_danh_muc` int DEFAULT NULL,
  `gia_san_pham` int DEFAULT NULL,
  `so_luong_ton_kho` int DEFAULT '0',
  `mo_ta_san_pham` varchar(1000) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `gia_nhap_san_pham` int DEFAULT '0',
  PRIMARY KEY (`id_san_pham`),
  KEY `id_danh_muc_idx` (`id_danh_muc`),
  CONSTRAINT `id_danh_muc` FOREIGN KEY (`id_danh_muc`) REFERENCES `danh_muc_san_pham` (`id_danh_muc`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_sach_san_pham`
--

LOCK TABLES `danh_sach_san_pham` WRITE;
/*!40000 ALTER TABLE `danh_sach_san_pham` DISABLE KEYS */;
INSERT INTO `danh_sach_san_pham` VALUES (1,'Áo len sọc trắng tím',1,100000,85,'Áo chất liệu len, họa tiết sọc màu trắng tím xen kẻ',15000),(2,'Áo khoác jean tím',1,200000,25,'Áo khoác jeans tím thời thượng, cổ bẻ, nút bấm tiện lợi, có túi ngực. Phong cách trẻ trung, dễ phối đồ.',50000),(3,'Áo khoác lông màu hồng',1,100000,30,'Áo khoác lông màu hồng thời trang, cổ lông cao cấp, khóa kéo tiện lợi, có túi bên. Thiết kế sang trọng, ấm áp, lý tưởng cho mùa lạnh.',20000),(4,'Quần dài màu be đậm',2,300000,50,'Quần jogger màu be thời trang, chất liệu mềm mại, cạp thun kèm dây rút, có túi bên. Thiết kế thoải mái, phù hợp cho phong cách hàng ngày.',50000),(5,'Áo khoác dài màu be đậm',1,600000,66,'Áo trench coat màu nâu thanh lịch, thiết kế cổ cao, đai thắt eo, nút cài tinh tế. Chất liệu cao cấp, phù hợp cho phong cách sang trọng mùa đông.',50000),(6,'Mũ len màu hồng',5,100000,20,'Mũ len hồng phấn, đan họa tiết, ấm áp, phong cách mùa đông.',50000),(7,'Áo khoác dài màu bạc đậm',1,200000,27,'Áo trench coat xám tinh tế, đai thắt eo, nút cài, dáng thanh lịch.',20000),(8,'Áo bông màu trắng',1,300000,88,'Áo khoác lông trắng sang trọng, cổ cao, nút bấm, giữ ấm tốt.',25000),(9,'Áo khoác len màu trắng',1,200000,77,'Áo khoác lông trắng kem, cổ tròn, nút cài, phong cách mùa đông.',25000),(10,'Áo đỏ',1,300000,53,'Áo thun đỏ tươi, cổ tròn, tay ngắn, thoải mái, năng động.',25000),(11,'Quần Gradient Cam',2,50000,70,'Quần short họa tiết cam-vàng, cạp chun, dáng rộng, phù hợp mùa hè.',25000),(12,'Quần ngắn màu cam',2,100000,67,'Quần short cam, cạp chun, dáng rộng, trẻ trung, tiện lợi.',35000),(13,'Chân váy màu vàng nhạt',2,200000,90,'Váy xòe beige, xếp ly, dáng midi, thanh lịch, dễ phối đồ.',35000),(14,'Mũ xanh biển',5,900000,20,'Mũ rộng vành xanh lam, chất liệu rơm, nhẹ, phù hợp mùa hè.',35000),(15,'Mũ vàng',5,100000,90,'Mũ bucket vàng, dáng tròn, phong cách năng động, trẻ trung.',20000),(16,'Mũ quý bà màu tím',5,50000,50,'Mũ fedora tím, nơ trang trí, thanh lịch, phù hợp phong cách cổ điển.',10000),(17,'Mũ rơm có nơ đen',5,150000,0,'Mũ rộng vành vàng, nơ đen, chất liệu rơm, phong cách mùa hè.',15000),(18,'Mũ cao bồi',5,300000,0,'Mũ cao bồi beige, vành rộng, chất liệu nỉ, phong cách vintage.',30000),(19,'Mũ hồng',5,250000,0,'Mũ bowler hồng, dáng tròn, thời thượng, phù hợp phong cách nổi bật.',25000),(20,'Mũ cao bồi đậm',5,550000,0,'Mũ cao bồi nâu, chất liệu da, vành rộng, phong cách bụi bặm.',55000),(21,'Mũ cao bồi viền cam',5,1000000,0,'Mũ cao bồi nâu, vành rộng, phong cách bụi bặm.',100000),(22,'Áo khoác dài sọc caro màu cam',1,100000,0,'Áo khoác caro cam-nâu, dáng dài, nút cài, thanh lịch.',10000),(23,'',1,850000,0,'',85000),(24,'Áo khoác dù',1,1200000,0,'Áo dù cam-đen, cổ cao, khóa kéo, giữ ấm tốt.',120000),(25,'Mũ rơm',5,900000,0,'Mũ rơm màu beige, vành rộng, kiểu dáng mùa hè.',90000),(26,'Mũ sombrero',5,950000,0,'Mũ sombrero nhiều màu, vành rộng, phong cách truyền thống.',95000),(27,'Giày thể thao trắng hồng',3,1200000,0,'Giày thể thao trắng hồng, đế êm, phong cách năng động.',120000),(28,'Giày thể thao tím',3,600000,0,'Giày thể thao tím, thiết kế đơn giản, thoải mái.',60000),(29,'Giày công sở',3,700000,0,'Giày da đen, dáng cổ điển, phù hợp công sở.',70000),(30,'Giày thể thao xanh dương',3,800000,0,'Giày thể thao xanh dương, đế trắng, năng động.',80000),(31,'Giày thể thao trắng đỏ',3,300000,0,'Giày thể thao xám-đỏ, phong cách hiện đại, thoải mái.',30000),(32,'Giày thể thao xám xanh',3,400000,0,'Giày thể thao xám-xanh, đế êm, phù hợp chạy bộ.',40000),(33,'Giày thể thao đỏ',3,100000,0,'Giày thể thao đỏ, thiết kế trẻ trung, năng động.',10000),(34,'Áo khoác lông',1,150000,0,'Áo khoác lông nâu, cổ lông, dáng dài, sang trọng.',15000),(35,'Áo blazer',1,100000,0,'Áo blazer xám, dáng ôm, nút cài, phong cách công sở.',10000),(36,'Giày thể thao trắng xanh',3,70000,0,'Giày thể thao trắng-xanh, đế êm, phong cách năng động.',7000),(37,'Giày Sneaker',3,150000,0,'Giày sneaker nâu, dáng cổ thấp, trẻ trung.',15000),(38,'Quần jean đen',2,200000,0,'Quần jeans đen, dáng ôm, phong cách hiện đại.',20000),(39,'Quần kaki xanh',2,200000,0,'Quần kaki xanh lá, dáng suông, thoải mái.',20000),(40,'Quần kaki beige',2,450000,0,'Quần kaki beige, dáng suông, thanh lịch.',45000),(41,'Quần cargo beige',2,350000,0,'Quần cargo beige, nhiều túi, phong cách năng động.',35000),(42,'Quần cargo xanh',2,400000,0,'Quần cargo xanh lá, dáng rộng, nhiều túi, bụi bặm.',40000),(43,'Quần short kaki xanh',2,195000,0,'Quần short kaki xanh lá, cạp chun, dáng rộng, thoải mái.',19000),(44,'Quần short đỏ',2,293000,0,'Quần short đỏ, cạp chun, phong cách năng động.',22900),(45,'Áo thun xanh dương',1,391000,0,'Áo thun xanh dương, cổ tròn, tay ngắn, trẻ trung.',39000),(46,'Áo len xám',1,498000,0,'Áo len xám, cổ tròn, phong cách tối giản.',50000),(47,'Áo khoác hồng phấn',1,391000,0,'Áo khoác hồng phấn, khóa kéo, dáng thể thao.',39000),(48,'Áo thun xanh lá',1,780000,0,'Áo thun xanh lá, cổ tròn, tay ngắn, năng động.',80000),(49,'Áo khoác dù vàng',1,350000,0,'Áo khoác dù vàng, có mũ, dáng dài, chống thấm tốt.',40000),(50,'Quần dài đỏ',2,180000,0,'Quần dài đỏ, dáng suông, phong cách nổi bật.',20000),(51,'Quần cargo xám',2,480000,0,'Quần cargo xám, nhiều túi, dáng rộng, năng động.',400000),(52,'Quần jogger vàng',2,350000,0,'Quần jogger vàng, cạp chun, dáng ôm, trẻ trung.',300000),(53,'Quần jeans xanh',2,350000,0,'Quần jeans xanh, dáng ôm, phong cách hiện đại.',300000),(54,'Quần short caro',2,320000,0,'Quần short caro xanh-đen, cạp chun, dáng rộng.',300000),(55,'Quần short thể thao',2,320000,0,'Quần short thể thao xanh-đỏ, cạp chun, năng động.',300000),(56,'Quần short xám',2,280000,0,'Quần short xám, cạp chun, phong cách tối giản.',200000),(57,'Áo len nâu',1,250000,0,'Áo len nâu, cổ tròn, họa tiết, ấm áp.',200000),(58,'Quần short hồng',2,320000,0,'Quần short hồng, cạp chun, dáng rộng, nổi bật.',300000),(59,'Quần short kẻ',2,320000,0,'Quần short kẻ xanh-trắng, cạp chun, phong cách mùa hè.',300000),(60,'Áo trench coat',1,450000,0,'Áo trench coat hồng, đai thắt, dáng dài, thanh lịch.',400000),(61,'Quần short cargo xanh lá',2,320000,0,'Quần short cargo xanh lá, nhiều túi, phong cách năng động.',300000),(62,'Quần short beige',2,320000,0,'Quần short beige, cạp chun, dáng suông, phong cách thoải mái.',300000),(63,'Mũ fedora đen',5,499000,0,'Mũ fedora đen, huy hiệu trang trí, phong cách cổ điển.',400000),(64,'Mũ chóp đen',5,499000,0,'Mũ chóp cao đen, dáng cao, phong cách lịch lãm.',400000),(65,'Mũ rơm beige',5,999000,0,'Mũ rơm beige, vành rộng, họa tiết, phù hợp mùa hè.',800000),(66,'Mũ sombroro nhiều màu',5,499000,0,'Mũ sombrero nhiều màu, vành rộng, phong cách truyền thống.',400000),(67,'Mũ cao bồi đỏ',5,2490000,0,'Mũ cao bồi đỏ, vành rộng, phong cách nổi bật.',1600000),(68,'Áo len nâu vàng',1,360000,0,'Áo len nâu-vàng, cổ tròn, phong cách mùa đông.',300000),(69,'Mũ bảo hộ',5,150000,0,'Mũ bảo hộ vàng, chất liệu nhựa, bảo vệ an toàn.',100000),(70,'Mũ cảnh sát',5,150000,0,'Mũ cảnh sát xanh đen, huy hiệu, phong cách chuyên nghiệp.',100000),(71,'Mũ hề',5,100000,0,'Mũ hề đỏ, dáng xoăn, phong cách hóa trang vui nhộn.',100000),(72,'Áo dù vàng',1,260000,0,'Áo khoác dù vàng, có mũ, dáng ngắn, chống thấm tốt.',200000),(73,'Mũ lưỡi trai nâu',5,160000,0,'Mũ lưỡi trai nâu, họa tiết caro, phong cách cổ điển.',100000),(74,'Mũ lưỡi trai xanh lá',5,160000,0,'Mũ lưỡi trai xanh lá, dáng thể thao, năng động.',100000),(75,'Giày sneaker trắng',3,320000,0,'Giày sneaker trắng, đế êm, phong cách tối giản.',300000),(76,'Giày sneaker xanh trắng',3,320000,0,'Giày sneaker xanh-trắng, đế trắng, trẻ trung.',300000),(77,'Giày boot đen',3,450000,0,'Giày boot đen, cổ cao, phong cách mạnh mẽ.',400000),(78,'Giày da nâu',3,400000,0,'Giày da nâu, dáng cổ điển, thanh lịch.',360000),(79,'Mũ len beige',5,240000,0,'Mũ len beige, đan họa tiết, ấm áp, mùa đông.',200000),(80,'Giày Sneaker trắng',3,360000,0,'Giày sneaker trắng, đế trắng, phong cách năng động.',300000),(81,'Áo trench coat hồng phấn',1,1200000,0,'Áo trench coat hồng phấn, đai thắt, dáng dài, thanh lịch.',800000),(82,'Áo khoác đỏ',1,350000,0,'Áo khoác đỏ, cổ cao, phong cách cứu hỏa chuyên nghiệp.',300000),(83,'Áo khoác dù nâu',1,350000,0,'Áo khoác dù nâu, cổ cao, khóa kéo, giữ ấm tốt.',300000),(84,'Áo khoác da đen',1,420000,0,'Áo khoác da đen, dáng ôm, phong cách cá tính.',400000),(85,'Áo khoác da đen',1,420000,0,'Áo khoác da đen, cổ cao, khóa kéo, mạnh mẽ.',400000),(86,'Áo khoác xanh lá',1,420000,0,'Áo khoác xanh lá, có mũ, dáng ngắn, năng động.',400000),(87,'Áo polo cam',1,360000,0,'Áo polo cam, cổ bẻ, tay ngắn, phong cách thể thao.',300000),(88,'Áo khoác da nâu',1,420000,0,'Áo khoác da nâu, dáng ôm, phong cách bụi bặm.',400000),(89,'Áo khoác đỏ trắng',1,450000,0,'Áo khoác đỏ-trắng, khóa kéo, phong cách thể thao.',400000),(90,'Áo len trắng',1,280000,0,'Áo len trắng, lông xù, dáng ôm, ấm áp.',200000),(91,'Áo khoác xanh trắng',1,320000,0,'Áo khoác xanh-trắng, khóa kéo, phong cách varsity trẻ trung.',300000),(92,'Áo len xanh lá',1,320000,0,'Áo len xanh lá, dáng rộng, phong cách thoải mái.',300000);
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
  `loai_hoa_don` varchar(45) DEFAULT NULL,
  `ngay_giao_dich` date DEFAULT NULL,
  PRIMARY KEY (`id_hoa_don`),
  UNIQUE KEY `id_hoa_don_UNIQUE` (`id_hoa_don`),
  KEY `id_khach_hang_idx` (`id_khach_hang`),
  CONSTRAINT `id_khach_hang` FOREIGN KEY (`id_khach_hang`) REFERENCES `danh_sach_khach_hang` (`id_khach_hang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_su_hoa_don`
--

LOCK TABLES `lich_su_hoa_don` WRITE;
/*!40000 ALTER TABLE `lich_su_hoa_don` DISABLE KEYS */;
INSERT INTO `lich_su_hoa_don` VALUES (1,600000,0,'M','2025-05-14'),(2,1000000,0,'M','2025-05-14'),(3,1500000,0,'M','2025-05-14'),(4,1500000,1,'B','2025-05-14'),(5,1000000,2,'B','2025-05-14'),(6,600000,0,'M','2025-05-15'),(7,3000000,0,'M','2025-05-15'),(8,3500000,0,'M','2025-05-15'),(9,1000000,0,'M','2025-05-15'),(10,600000,0,'M','2025-05-15'),(11,2250000,0,'M','2025-05-15'),(12,2000000,0,'M','2025-05-15'),(13,1375000,0,'M','2025-05-15'),(14,1750000,0,'M','2025-05-15'),(15,2345000,0,'M','2025-05-15'),(16,3150000,0,'M','2025-05-15'),(17,700000,0,'M','2025-05-15'),(18,2000000,0,'M','2025-05-15'),(19,1000000,8,'B','2025-05-15'),(20,3800000,10,'B','2025-05-15'),(21,500000,0,'M','2025-05-15'),(22,4000000,30,'B','2025-05-15');
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

-- Dump completed on 2025-05-15  2:53:13
