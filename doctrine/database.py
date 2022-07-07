import sqlite3

from core import config


def create_doctrine(eft_dict: dict, required: int) -> int:
    """Write the eft_dict to database as a doctrine.
    Set the required parameter as the quantity required to keep in stock

    :param eft_dict: dict a fit as returned by reserves.utils.parsers.parse_eft()
    :param required: int the quantity required to keep in stock
    :return: int the doctrine id of the new doctrine
    """

    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM doctrine;")
    max_id = c.fetchone()[0]
    if max_id:
        doctrine_id = int(max_id) + 1
    else:
        doctrine_id = 1
    c.execute("INSERT INTO doctrine VALUES (?,?,?);", (doctrine_id, eft_dict['name'], required))

    for name, required in eft_dict['items'].items():
        c.execute("SELECT id FROM item WHERE name=?;", (name,))
        item_id = c.fetchone()[0]
        c.execute("INSERT INTO doctrine_item VALUES (?,?,?);", (doctrine_id, item_id, required))
    conn.commit()
    c.close()
    conn.close()
    return doctrine_id


def get_doctrine(doctrine_id: int) -> dict:
    """Retrieve data for the fit of the given doctrine_id.

    Example output:

        {
            'name': Tempest Fleet Issue,
            'required': 100,
            'available: 50,
            'items': {
                'name': name,
                'required': required,
                'available': available,
                'items': items
            }
        }

    :param doctrine_id: int the id of the fit
    :return: dict Ship fitting in dict format
    """

    # Create connection
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    # Get the doctrine name and required quantity
    c.execute("SELECT name, required FROM doctrine WHERE id=?;", (doctrine_id,))
    doctrine_name, doctrine_required = c.fetchone()

    # Get doctrine availability
    c.execute("SELECT MIN(item.available / doctrine_item.required) FROM doctrine_item, item WHERE doctrine_item.item_id=item.id AND doctrine_id=?;", (doctrine_id,))
    doctrine_available = c.fetchone()[0]

    doctrine_percent = min(int(doctrine_available / doctrine_required * 100), 100)

    # Get all items for this doctrine
    c.execute("SELECT item.name, doctrine_item.required, item.available, item.price FROM doctrine, item, doctrine_item WHERE doctrine.id=? AND doctrine_item.doctrine_id=? AND doctrine_item.item_id=item.id;", (doctrine_id, doctrine_id))
    doctrine_price = 0
    items = []
    for item in c.fetchall():
        item_name, item_required, item_available, item_price = item
        item = {
            'name': item_name,
            'required': item_required,
            'available': item_available,
            'unit_price': item_price,
            'total_price': item_price * item_required
        }
        doctrine_price += item_required + item_price
        items.append(item)

    doctrine = {
        'id': doctrine_id,
        'name': doctrine_name,
        'required': doctrine_required,
        'available': doctrine_available,
        'percent': doctrine_percent,
        'price': doctrine_price,
        'items': items
    }

    # Close connection
    c.close()
    conn.close()
    return doctrine


def list_doctrines():
    """Retrieve all doctrines and related stats

    Example output:
        [
            {
                'id': 1,
                'name': 'Ferox',
                'required': 50,
                'available': 104,
                'percent': 100
            },
        ]

    :return: list[dict]
    """

    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT doctrine.id, doctrine.name, doctrine.required, MIN(item.available/doctrine_item.required) FROM doctrine, doctrine_item, item WHERE doctrine.id=doctrine_item.doctrine_id AND doctrine_item.item_id=item.id GROUP BY doctrine.id;")
    doctrines = []
    for doctrine in c.fetchall():
        id, name, required, available = doctrine
        percent = min(int(available / required * 100), 100)
        d = {
            'id': id,
            'name': name,
            'required': required,
            'available': available,
            'percent': percent,
        }
        doctrines.append(d)

    doctrines = sorted(doctrines, key=lambda d: d['percent'])

    conn.commit()
    c.close()
    conn.close()
    return doctrines


def update_doctrine(doctrine_id: int, eft_dict: dict = None, required: int = None) -> int:
    # no changes passed in
    if not required and not eft_dict:
        return doctrine_id

    # only update required
    if required and not eft_dict:
        conn = sqlite3.connect(config.DATABASE_PATH)
        c = conn.cursor()
        c.execute("UPDATE doctrine SET required=? WHERE id=?;", (required, doctrine_id))
        conn.commit()
        c.close()
        conn.close()
        return doctrine_id

    # only update fit
    if eft_dict and not required:
        conn = sqlite3.connect(config.DATABASE_PATH)
        c = conn.cursor()
        c.execute("SELECT required FROM doctrine WHERE id=?;", (doctrine_id,))
        required = c.fetchone()[0]
        conn.commit()
        c.close()
        conn.close()
        return create_doctrine(eft_dict, required)

    # update both
    delete_doctrine(doctrine_id)
    return create_doctrine(eft_dict, required)


def delete_doctrine(doctrine_id: int):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM doctrine_item WHERE doctrine_id=?;", (doctrine_id,))
    c.execute("DELETE FROM doctrine WHERE id=?;", (doctrine_id,))
    conn.commit()
    c.close()
    conn.close()


def get_doctrine_items():
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT item.name, SUM(doctrine.required * doctrine_item.required) AS required, item.available, item.price FROM doctrine, doctrine_item, item WHERE doctrine.id=doctrine_item.doctrine_id AND doctrine_item.item_id=item.id GROUP BY doctrine_item.item_id;")
    items = []
    for item in c.fetchall():
        name, required, available, price = item
        percent = min(int(available / required * 100), 100)
        d = {
            'name': name,
            'required': required,
            'available': available,
            'percent': percent,
            'price': price
        }
        items.append(d)

    # sort by percent
    items = sorted(items, key=lambda item: item['percent'])

    conn.commit()
    c.close()
    conn.close()
    return items


def get_missing_items():
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    # Get all items that are below required threshold
    c.execute("SELECT item.name, SUM(doctrine.required * doctrine_item.required) - item.available as short FROM doctrine, doctrine_item, item WHERE doctrine.id=doctrine_item.doctrine_id AND doctrine_item.item_id=item.id GROUP BY doctrine_item.item_id HAVING short > 0;")
    items = []
    for item in c.fetchall():
        name, missing = item
        d = {
            'name': name,
            'missing': missing
        }
        items.append(d)

    # Close connection
    conn.commit()
    c.close()
    conn.close()
    return items
