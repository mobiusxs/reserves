import sqlite3

from core import config


def main():
    """Build all tables contained within schema.sql"""

    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    schema = open('schema.sql')
    c.executescript(schema.read())
    conn.commit()
    schema.close()
    c.close()
    conn.close()


if __name__ == '__main__':
    main()
