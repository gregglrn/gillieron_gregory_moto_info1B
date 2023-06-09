-- --------------------------------------------------------
-- Hôte :                        127.0.0.1
-- Version du serveur:           5.7.40 - MySQL Community Server (GPL)
-- SE du serveur:                Win32
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Listage de la structure de la base pour gillieron_gregory_bd_info1b
CREATE DATABASE IF NOT EXISTS `gillieron_gregory_bd_info1b` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `gillieron_gregory_bd_info1b`;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_adresse
CREATE TABLE IF NOT EXISTS `t_adresse` (
  `id_adresse` int(11) NOT NULL AUTO_INCREMENT,
  `adresse_personne` varchar(50) DEFAULT NULL,
  `ville_personne` varchar(50) DEFAULT NULL,
  `code_postale_personne` int(11) DEFAULT NULL,
  `pays_personne` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_adresse`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_adresse : ~0 rows (environ)
/*!40000 ALTER TABLE `t_adresse` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_adresse` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_entrepot
CREATE TABLE IF NOT EXISTS `t_entrepot` (
  `id_entrepot` int(11) NOT NULL AUTO_INCREMENT,
  `place_entrepot` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_entrepot`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_entrepot : ~0 rows (environ)
/*!40000 ALTER TABLE `t_entrepot` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_entrepot` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_mail
CREATE TABLE IF NOT EXISTS `t_mail` (
  `id_mail` int(11) NOT NULL AUTO_INCREMENT,
  `mail_personne` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_mail`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_mail : ~0 rows (environ)
/*!40000 ALTER TABLE `t_mail` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_mail` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_marque
CREATE TABLE IF NOT EXISTS `t_marque` (
  `id_marque` int(11) NOT NULL AUTO_INCREMENT,
  `marque_moto` varchar(50) DEFAULT NULL,
  `type_moto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_marque`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_marque : 6 rows
/*!40000 ALTER TABLE `t_marque` DISABLE KEYS */;
INSERT INTO `t_marque` (`id_marque`, `marque_moto`, `type_moto`) VALUES
	(6, 'kawasaki', 'Sportive'),
	(5, 'yamaha', 'Roadster'),
	(7, 'honda', 'Roadster'),
	(8, 'ducati', 'Sportive'),
	(9, 'triumph', 'Roadster'),
	(10, 'ktm', 'Sportive'),
	(13, 'yamaha', 'supermot'),
	(14, 'yamaha', 'Sportive'),
	(15, 'bmw', 'Sportive');
/*!40000 ALTER TABLE `t_marque` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_marque_moto
CREATE TABLE IF NOT EXISTS `t_marque_moto` (
  `id_marque_moto` int(11) NOT NULL AUTO_INCREMENT,
  `fk_marque` int(11) DEFAULT NULL,
  `fk_moto` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_marque_moto`),
  KEY `FK_t_marque_moto_t_marque` (`fk_marque`),
  KEY `FK_t_marque_moto_t_moto` (`fk_moto`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_marque_moto : 1 rows
/*!40000 ALTER TABLE `t_marque_moto` DISABLE KEYS */;
INSERT INTO `t_marque_moto` (`id_marque_moto`, `fk_marque`, `fk_moto`) VALUES
	(14, 10, 10),
	(13, 5, 9),
	(15, 6, 12),
	(16, 6, 13),
	(17, 10, 14),
	(18, 15, 15),
	(19, 13, 16),
	(20, 13, 11);
/*!40000 ALTER TABLE `t_marque_moto` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_moto
CREATE TABLE IF NOT EXISTS `t_moto` (
  `id_moto` int(11) NOT NULL AUTO_INCREMENT,
  `modèle_moto` varchar(50) DEFAULT NULL,
  `année_moto` year(4) DEFAULT NULL,
  `nombre_km_moto` varchar(50) DEFAULT NULL,
  `prix_moto` varchar(50) DEFAULT NULL,
  `état_moto` varchar(50) DEFAULT NULL,
  `couleur_moto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_moto`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_moto : ~0 rows (environ)
/*!40000 ALTER TABLE `t_moto` DISABLE KEYS */;
INSERT INTO `t_moto` (`id_moto`, `modèle_moto`, `année_moto`, `nombre_km_moto`, `prix_moto`, `état_moto`, `couleur_moto`) VALUES
	(9, 'MT-125', '2021', '10000km', '12000.-', NULL, 'Noir'),
	(10, 'DUKE-125', '2023', '0km', '4999.-', NULL, 'Orange'),
	(11, 'YZF-R7', '2022', '10000km', '12000.-', NULL, 'Bleu'),
	(12, 'H2', '2022', '6468km', '18099.-', NULL, 'vert'),
	(13, 'Z900', '2020', '0km', '16899.-', NULL, 'Noir'),
	(14, 'RC125', '2022', '0km', '4999.-', NULL, 'blanc'),
	(15, 'S1000RR', '2019', '1942km', '32000.-', NULL, 'Bleu'),
	(16, 'YZF-R1', '2022', '0km', '19999.-', NULL, 'Bleu');
/*!40000 ALTER TABLE `t_moto` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_moto_entrepot
CREATE TABLE IF NOT EXISTS `t_moto_entrepot` (
  `id_moto_entrepot` int(11) NOT NULL AUTO_INCREMENT,
  `fk_entrepot` int(11) DEFAULT NULL,
  `fk_moto` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_moto_entrepot`),
  KEY `fk_entrepot` (`fk_entrepot`),
  KEY `fk_moto` (`fk_moto`),
  CONSTRAINT `FK_t_moto_entrepot_t_entrepot` FOREIGN KEY (`fk_entrepot`) REFERENCES `t_entrepot` (`id_entrepot`),
  CONSTRAINT `FK_t_moto_entrepot_t_moto` FOREIGN KEY (`fk_moto`) REFERENCES `t_moto` (`id_moto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_moto_entrepot : ~0 rows (environ)
/*!40000 ALTER TABLE `t_moto_entrepot` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_moto_entrepot` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_personne
CREATE TABLE IF NOT EXISTS `t_personne` (
  `id_personne` int(11) NOT NULL AUTO_INCREMENT,
  `prenom_personne` varchar(50) DEFAULT NULL,
  `nom_personne` varchar(50) DEFAULT NULL,
  `date_naissance_personne` date DEFAULT NULL,
  `sexe_personne` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_personne : ~1 rows (environ)
/*!40000 ALTER TABLE `t_personne` DISABLE KEYS */;
INSERT INTO `t_personne` (`id_personne`, `prenom_personne`, `nom_personne`, `date_naissance_personne`, `sexe_personne`) VALUES
	(5, 'fgfgh', NULL, NULL, NULL),
	(7, 'mathis', NULL, NULL, NULL);
/*!40000 ALTER TABLE `t_personne` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_pers_adresse
CREATE TABLE IF NOT EXISTS `t_pers_adresse` (
  `id_pers_adresse` int(11) NOT NULL AUTO_INCREMENT,
  `fk_adresse` int(11) DEFAULT NULL,
  `fk_personne` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_adresse`),
  KEY `fk_adresse` (`fk_adresse`),
  KEY `fk_personne` (`fk_personne`),
  CONSTRAINT `FK_t_pers_adresse_t_adresse` FOREIGN KEY (`fk_adresse`) REFERENCES `t_adresse` (`id_adresse`),
  CONSTRAINT `FK_t_pers_adresse_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_pers_adresse : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_adresse` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_adresse` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_pers_mail
CREATE TABLE IF NOT EXISTS `t_pers_mail` (
  `id_pers_mail` int(11) NOT NULL AUTO_INCREMENT,
  `fk_mail` int(11) DEFAULT NULL,
  `fk_personne` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_mail`),
  KEY `fk_mail` (`fk_mail`),
  KEY `fk_personne` (`fk_personne`),
  CONSTRAINT `FK_t_pers_mail_t_mail` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`),
  CONSTRAINT `FK_t_pers_mail_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_pers_mail : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_mail` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_mail` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_pers_moto
CREATE TABLE IF NOT EXISTS `t_pers_moto` (
  `id_pers_moto` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_moto` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_moto`),
  KEY `fk_personne` (`fk_personne`),
  KEY `fk_moto` (`fk_moto`),
  CONSTRAINT `FK_t_pers_moto_t_moto` FOREIGN KEY (`fk_moto`) REFERENCES `t_moto` (`id_moto`),
  CONSTRAINT `FK_t_pers_moto_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_pers_moto : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_moto` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_moto` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_pers_telephone
CREATE TABLE IF NOT EXISTS `t_pers_telephone` (
  `id_pers_telephone` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_telephone` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_telephone`),
  KEY `fk_personne` (`fk_personne`),
  KEY `fk_telephone` (`fk_telephone`),
  CONSTRAINT `FK_t_pers_telephone_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`),
  CONSTRAINT `FK_t_pers_telephone_t_telephone` FOREIGN KEY (`fk_telephone`) REFERENCES `t_telephone` (`id_telephone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_pers_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_telephone` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_telephone` ENABLE KEYS */;

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_telephone
CREATE TABLE IF NOT EXISTS `t_telephone` (
  `id_telephone` int(11) NOT NULL AUTO_INCREMENT,
  `telephone_personne` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_telephone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_telephone` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_telephone` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
