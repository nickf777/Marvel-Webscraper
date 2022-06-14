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

DROP TABLE IF EXISTS character_details;
CREATE TABLE IF NOT EXISTS character_details (
	character_details_id INT NOT NULL AUTO_INCREMENT,
	first_appearance TEXT,
	based_on TEXT,
	adapted_by TEXT,
	portrayed_by TEXT ,
	voiced_by TEXT,
	alias TEXT,
	title TEXT,
	occupation TEXT,
	affiliation TEXT,
	weapon TEXT,
	significant_others TEXT,
	nationality TEXT,
	char_name TEXT,
	full_name TEXT,
	aliases TEXT,
	nicknames TEXT,
	origin TEXT,
	family TEXT,
	spouse TEXT,
	children TEXT,
	nickname TEXT,
	relatives TEXT,
	last_appearance TEXT,
	created_by TEXT,
	species TEXT,
	significant_other TEXT,
	motion_capture_by TEXT,
	publisher TEXT,
	alter_ego TEXT,
	team_affiliations TEXT,
	notable_aliases TEXT,
	abilities TEXT,
	position TEXT,
	partnerships TEXT,
	place_of_origin TEXT,
	supporting_character_of TEXT,
	home TEXT,
	schedule TEXT,
	format TEXT,
	genre TEXT,
	publication_date TEXT,
	number_of_issues TEXT,
	writer TEXT,
	penciller TEXT,
	creators TEXT,
	gender TEXT,
	written_by TEXT,
	inker TEXT,
	colorist TEXT,
	editor TEXT,
    PRIMARY KEY (character_details_id)
);

SELECT * FROM character_details;