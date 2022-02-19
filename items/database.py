import sqlite3

from core.config import DATABASE_PATH


def list_items():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT items.name, fits.quantity * fit_items.quantity AS required, items.volume FROM fits, fit_items, items WHERE fits.fit_id=fit_items.fit_id AND fit_items.type_id=items.type_id GROUP BY fit_items.type_id;")
    items = []
    for item in c.fetchall():
        name, required, available = item
        percentage = min(int(available / required * 100), 100)
        items.append((name, required, available, percentage))
    items = sorted(items, key=lambda t: t[3])
    conn.commit()
    c.close()
    conn.close()
    return items


def buy_all():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT items.name, fits.quantity * fit_items.quantity - items.volume as short FROM fits, fit_items, items WHERE fits.fit_id=fit_items.fit_id AND fit_items.type_id=items.type_id AND short > 0 GROUP BY fit_items.type_id;")
    items = [i for i in c.fetchall()]
    conn.commit()
    c.close()
    conn.close()
    return items
