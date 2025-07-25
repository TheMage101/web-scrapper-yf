CREATE TABLE News (
    Link VARCHAR(255) UNIQUE,
    Article VARCHAR(100000),
    ArticleTime TIMESTAMP,
    PRIMARY KEY(Link)
);

CREATE TABLE SICCodes (
    Code VARCHAR(10),
    CodeDescription VARCHAR(128),
    PRIMARY KEY (Code)
);

CREATE TABLE Company (
    Ticker VARCHAR(10),
    NewsLink VARCHAR(255),
    PRIMARY KEY(Ticker, NewsLink),
    FOREIGN KEY (NewsLink) REFERENCES News (Link)
);

CREATE TABLE CompanyValues (
    Ticker VARCHAR(10),
    ValueTime TIMESTAMP,
    ValuePrice NUMBER(15,5),
    FOREIGN KEY (Ticker) REFERENCES Company (Ticker)
);