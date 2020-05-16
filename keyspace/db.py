import sqlite3
from flask import g

from . import config

def get_db():
    db = getattr(g, "database", None)
    if db is None:
        db = g.database = sqlite3.connect(config.db_path)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def cleanup(*args):
    db = getattr(g, "database", None)
    if db is not None:
        db.close()
