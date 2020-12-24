from flask import g
from database.mymongodb import MyMongoDB


def get_db(db_name=None, url=None):
    if 'db' not in g:
        g.db = MyMongoDB(db_name, url)

    return g.db


def init_db(db_name, url):
    db = get_db(db_name=db_name, url=url)
    return db

