-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           10.10.2-MariaDB - mariadb.org binary distribution
-- SE du serveur:                Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour bdetu
CREATE DATABASE IF NOT EXISTS `bdetu` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `bdetu`;

-- Listage de la structure de la table bdetu. etudiants
CREATE TABLE IF NOT EXISTS `etudiants` (
  `id` varchar(50) NOT NULL DEFAULT 'none',
  `surname` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `year` varchar(50) DEFAULT NULL,
  `global_moy` float DEFAULT NULL,
  `photo` longblob DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Listage des données de la table bdetu.etudiants : ~2 rows (environ)
/*!40000 ALTER TABLE `etudiants` DISABLE KEYS */;
/*!40000 ALTER TABLE `etudiants` ENABLE KEYS */;

-- Listage de la structure de la table bdetu. matières
CREATE TABLE IF NOT EXISTS `matières` (
  `id` varchar(50) DEFAULT NULL,
  `subject` varchar(50) DEFAULT NULL,
  `moy` float DEFAULT NULL,
  KEY `stud_id` (`id`),
  CONSTRAINT `stud_id` FOREIGN KEY (`id`) REFERENCES `etudiants` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Listage des données de la table bdetu.matières : ~3 rows (environ)
/*!40000 ALTER TABLE `matières` DISABLE KEYS */;
/*!40000 ALTER TABLE `matières` ENABLE KEYS */;

-- Listage de la structure de la table bdetu. users
CREATE TABLE IF NOT EXISTS `users` (
  `identifiant` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Listage des données de la table bdetu.users : ~1 rows (environ)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
REPLACE INTO `users` (`identifiant`, `password`) VALUES
	('admin', 'admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
