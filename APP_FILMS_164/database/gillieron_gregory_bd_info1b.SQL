-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: gillieron_gregory_bd_info1b

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS gillieron_gregory_bd_info1b;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS gillieron_gregory_bd_info1b;

-- Utilisation de cette base de donnée

USE gillieron_gregory_bd_info1b;
-- --------------------------------------------------------
-- --------------------------------------------------------
-- Hôte :                        localhost
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
  `place_entrepot` varchar(50) DEFAULT NULL,
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

-- Listage de la structure de la table gillieron_gregory_bd_info1b. t_moto
CREATE TABLE IF NOT EXISTS `t_moto` (
  `id_moto` int(11) NOT NULL AUTO_INCREMENT,
  `marque_moto` varchar(50) DEFAULT NULL,
  `modèle_moto` varchar(50) DEFAULT NULL,
  `année_moto` int(11) DEFAULT NULL,
  `nombre_km_moto` int(11) DEFAULT NULL,
  `prix_moto` float DEFAULT NULL,
  `état_moto` varchar(50) DEFAULT NULL,
  `couleur_moto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_moto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_moto : ~0 rows (environ)
/*!40000 ALTER TABLE `t_moto` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_personne : ~0 rows (environ)
/*!40000 ALTER TABLE `t_personne` DISABLE KEYS */;
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
  `numero_telephone_personne` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_telephone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table gillieron_gregory_bd_info1b.t_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_telephone` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_telephone` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
