CREATE TABLE crawler (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	domain VARCHAR(80),
	url VARCHAR(512),
	user_agent VARCHAR(256),
    crawl_time INT
);

