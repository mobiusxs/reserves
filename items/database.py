import sqlite3

from core.config import DATABASE_PATH


def list_items():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT item.name, doctrine.required * doctrine_item.required AS required, item.available FROM doctrine, doctrine_item, item WHERE doctrine.id=doctrine_item.doctrine_id AND doctrine_item.item_id=item.id GROUP BY doctrine_item.item_id;")
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
    c.execute("SELECT item.name, doctrine.required * doctrine_item.required - item.available as short FROM doctrine, doctrine_item, item WHERE doctrine.id=doctrine_item.doctrine_id AND doctrine_item.item_id=item.id AND short > 0 GROUP BY doctrine_item.item_id;")
    items = [i for i in c.fetchall()]
    conn.commit()
    c.close()
    conn.close()
    return items
