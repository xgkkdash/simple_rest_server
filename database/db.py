import sqlite3


def init_db():  # return a db with default table created
    db = sqlite3.connect('mydatabase.db')
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS kvpairs")
    cursor.execute("CREATE TABLE kvpairs(key text PRIMARY KEY, value text)")
    db.commit()

    return db

