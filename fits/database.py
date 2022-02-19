import sqlite3

from core import config
from data.select import get_by_name


def create_fit(fit, quantity):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT MAX(fit_id) FROM fits;")
    max_id = c.fetchone()[0]
    if max_id:
        fit_id = int(max_id) + 1
    else:
        fit_id = 1
    c.execute("INSERT INTO fits VALUES (?,?,?);", (fit_id, fit['name'], quantity))

    for name, quantity in fit['items'].items():
        type_id = get_by_name(name)[0]
        c.execute("INSERT INTO fit_items VALUES (?,?,?);", (fit_id, type_id, quantity))
    conn.commit()
    c.close()
    conn.close()
    return fit_id


def read_fit(fit_id):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT name, quantity FROM fits WHERE fit_id=?;", (fit_id,))
    name, required = c.fetchone()
    fit = {"name": name, 'required': required, 'items': {}}

    c.execute("SELECT MIN(items.volume / fit_items.quantity) FROM fit_items, items WHERE fit_items.type_id=items.type_id AND fit_id=?;", (fit_id,))
    fit['available'] = c.fetchone()[0]

    c.execute("SELECT items.name, fit_items.quantity, items.volume, items.price FROM fits, items, fit_items WHERE fits.fit_id=? AND fit_items.fit_id=? AND fit_items.type_id=items.type_id;", (fit_id, fit_id))
    for item in c.fetchall():
        name, required, available, price = item
        fit['items'][name] = {'required': required, 'available': available, 'price': price}

    c.close()
    conn.close()
    return fit


def list_fits():
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT fits.fit_id, fits.name, fits.quantity, MIN(items.volume/fit_items.quantity) FROM fits, fit_items, items WHERE fits.fit_id=fit_items.fit_id AND fit_items.type_id=items.type_id GROUP BY fits.fit_id;")
    fits = [i for i in c.fetchall()]
    conn.commit()
    c.close()
    conn.close()
    return fits
