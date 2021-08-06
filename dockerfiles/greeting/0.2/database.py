import psycopg2 as pg
import os

"""
Database (Postgres) module connecting to the database for the simple greeting
app.
"""

# The hostname where the database is running can be determined via environment
PGHOST = os.getenv("PG_HOST") if os.getenv("PG_HOST") else "localhost"


def get_pgconn():
    """
    Connects to the database and also triggers the creation of the single
    required table if it does not exist yet. Clearly you would not do
    that in a production environment.

    Returns
    -------
    psycopg2 database connection
    """
    # database credentials hard-coded except for hostname
    CRED = {
        "host": PGHOST,
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": "holymoly"
    }
    conn = pg.connect(**CRED)
    create(conn)
    return conn


def create(db):
    """
    helper function to create the required database table if it does not exist
    yet.

    Parameters
    ----------
    db: psycopg2 database connection
    """
    SQL_CREATE = """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL,
        message TEXT,
        author TEXT,
        received TEXT
    )
    """
    cursor = db.cursor()
    cursor.execute(SQL_CREATE)
    db.commit()


def insert(db, dct):
    """
    Inserts the entered data for author, message and timestamp into the
    database.

    Parameters
    ----------
    db: psycopg2 database connection
    dct: dict
        containing the fields message, author, received. Validity is not
        checked, every field is expected to be present and to contain a string
        as value.
    """
    SQL_INSERT = """
    INSERT INTO messages(message, author, received) VALUES (
        %(message)s,
        %(author)s,
        %(received)s
    )
    """
    cursor = db.cursor()
    cursor.execute(SQL_INSERT, dct)
    db.commit()
