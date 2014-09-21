CREATE USER 'shxreader'@'localhost' IDENTIFIED BY 'shxreader';

GRANT ALL ON shxreader.* TO 'shxreader'@'localhost';

CREATE TABLE owler (
	organization VARCHAR(80),
	owler_url VARCHAR(256),
	url VARCHAR(256),
    heading VARCHAR(256),
    timestamp INT
);
