CREATE DATABASE IF NOT EXISTS twitter;
USE twitter;
CREATE TABLE IF NOT EXISTS `tweets` (
	`hashtag` VARCHAR(64),
	`text` TINYTEXT,
	`date` DATETIME,
	`user` VARCHAR(64),
	`followers` INT,
	`location` VARCHAR(64),
	`language` VARCHAR(32)
);
ALTER TABLE `tweets` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;