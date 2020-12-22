import sqlite3

from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('mydatabase.db', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():  # return a db with default table created
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS kvpairs")
    cursor.execute("CREATE TABLE kvpairs(key text PRIMARY KEY, value text)")
    db.commit()

