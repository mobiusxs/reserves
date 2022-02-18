import sqlite3

from core import config


def get_by_id(type_id):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE type_id=?;", (type_id,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result


def get_by_name(type_name):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE name=?;", (type_name,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result
