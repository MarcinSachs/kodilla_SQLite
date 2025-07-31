import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database. Sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn


def add_album(conn, album):
   """
   Create new album into albums table
   :param conn:
   :param album:
   :return: album id
   """
   sql = '''INSERT INTO albums(name, release_date, artist_id, genre_id)
             VALUES(?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, album)
   conn.commit()
   return cur.lastrowid

def add_artist(conn, artist):
    sql = '''INSERT INTO artists(name)
             VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, artist)
    conn.commit()
    return cur.lastrowid

def add_genre(conn, genre):
    sql = '''INSERT INTO genres(name)
             VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, genre)
    conn.commit()
    return cur.lastrowid

def get_artist_id(conn, name):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM artists WHERE name = '{name}'")
    artist = cur.fetchone()
    if artist is None:
        artist_id = add_artist(conn, (name,))
        return artist_id
    return artist[0]

def get_genre_id(conn, name):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM genres WHERE name = '{name}'")
    genre = cur.fetchone()
    if genre is None:
        genre_id = add_genre(conn, (name,))
        return genre_id
    return genre[0]


