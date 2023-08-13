SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


DROP DATABASE IF EXISTS `sys`;
CREATE DATABASE IF NOT EXISTS `sys` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sys`;

-- --------------------------------------------------------

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS account(
   email VARCHAR(320) PRIMARY KEY,
   account_name VARCHAR(45) ,
   password VARCHAR(45)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `job`;
CREATE TABLE IF NOT EXISTS job(
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   jobname VARCHAR(45) ,
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `application`;
CREATE TABLE application (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(320) NULL,
  `jobid` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `email_idx` (`email` ASC) VISIBLE,
  INDEX `id_idx` (`jobid` ASC) VISIBLE,
  CONSTRAINT `email`
    FOREIGN KEY (`email`)
    REFERENCES `tap`.`account` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id`
    FOREIGN KEY (`jobid`)
    REFERENCES `tap`.`job` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);