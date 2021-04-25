DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS pagesInfo;

CREATE TABLE pagesInfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pageName TEXT NOT NULL,
    content TEXT NULL
);