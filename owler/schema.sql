CREATE USER 'shxreader'@'localhost' IDENTIFIED BY 'shxreader';

GRANT ALL ON shxreader.* TO 'shxreader'@'localhost';

CREATE TABLE owler (
	orgnization VARCHAR(80),
	owler_url VARCHAR(256),
	article_url VARCHAR(256),
    heading VARCHAR(256)
);
