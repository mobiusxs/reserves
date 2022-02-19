CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    available INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS doctrine (
    id INTEGER PRIMARY KEY,
    name TEXT,
    required INTEGER
);

CREATE TABLE IF NOT EXISTS doctrine_item (
    doctrine_id INTEGER,
    item_id INTEGER,
    required INTEGER,
    FOREIGN KEY(doctrine_id) REFERENCES doctrine(id),
    FOREIGN KEY(item_id) REFERENCES item(id)
);