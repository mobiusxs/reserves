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


def list_doctrines() -> list[dict]:
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
    # labels = 'id', 'name', 'required', 'available'
    # doctrines = [dict(zip(labels, i)) for i in c.fetchall()]
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
