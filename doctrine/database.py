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
    """Retrieve data for the fit of the given id.
    Example output:

        {
            'name': Tempest Fleet Issue,
            'required': 100,
            'available: 50,
            'items': [
                # (name, required, available, price)
                ('Damage Control II', 1, 1234, 1543000)
            ]
        }

    :param fit_id: int the id of the fit
    :return: dict Ship fitting in dict format
    """

    # Create connection
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    # Get the name and required quantity
    c.execute("SELECT name, quantity FROM fits WHERE fit_id=?;", (fit_id,))
    name, required = c.fetchone()

    # Get the availability of the fit
    c.execute("SELECT MIN(items.volume / fit_items.quantity) FROM fit_items, items WHERE fit_items.type_id=items.type_id AND fit_id=?;", (fit_id,))
    available = c.fetchone()[0]

    # get all fit items: (name, required, available, price)
    c.execute("SELECT items.name, fit_items.quantity, items.volume, items.price FROM fits, items, fit_items WHERE fits.fit_id=? AND fit_items.fit_id=? AND fit_items.type_id=items.type_id;", (fit_id, fit_id))
    items = [i for i in c.fetchall()]

    # Close connection
    c.close()
    conn.close()

    fit = {
        'name': name,
        'required': required,
        'available': available,
        'items': items
    }
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
