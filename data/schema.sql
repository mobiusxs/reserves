CREATE TABLE IF NOT EXISTS items (
    type_id INTEGER PRIMARY KEY,
    name TEXT,
    volume INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS fits (
    fit_id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS fit_items (
    fit_id INTEGER,
    type_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(fit_id) REFERENCES fits(fit_id),
    FOREIGN KEY(type_id) REFERENCES items(type_id)
);