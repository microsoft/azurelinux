CREATE TABLE resenders (
	host		TEXT,
	helo		TEXT,
	time		INTEGER,
    PRIMARY KEY (host, helo)
);

CREATE TABLE greylist (
	id		TEXT PRIMARY KEY,
	expire		INTEGER,
	host		TEXT,
	helo		TEXT
);
