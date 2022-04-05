CREATE SCHEMA IF NOT EXISTS marvel_database DEFAULT CHARACTER SET utf8mb4;

USE marvel_database;

CREATE TABLE IF NOT EXISTS characters (
	character_id INT NOT NULL AUTO_INCREMENT,
    char_name VARCHAR(65),
    char_type VARCHAR(65),
    char_desc MEDIUMTEXT,
    appearances MEDIUMTEXT,
    PRIMARY KEY (character_id)
);

SELECT * FROM characters;