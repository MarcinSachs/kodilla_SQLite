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
    except Error as e:
        print(e)
    return conn

def setup_database(conn):
    """Creates the necessary tables if they don't exist."""
    try:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            release_date TEXT NOT NULL,
            artist_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES artists (id),
            FOREIGN KEY (genre_id) REFERENCES genres (id),
            UNIQUE(name, artist_id)
        );
        """)
        conn.commit()
        print("Database tables are ready.")
    except Error as e:
        print(f"Error setting up database: {e}")

# CREATE
def add_album(conn, album_data):
   """
   Create a new album, artist, and genre if they don't exist.
   :param conn: Connection object
   :param album_data: a tuple containing (name, release_date, artist_name, genre_name)
   :return: album id
   """
   name, release_date, artist_name, genre_name = album_data
   try:
        artist_id = get_or_create_artist(conn, artist_name)
        genre_id = get_or_create_genre(conn, genre_name)
        sql = '''INSERT INTO albums(name, release_date, artist_id, genre_id)
             VALUES(?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (name, release_date, artist_id, genre_id))
        conn.commit()
        print(f"Album '{name}' added successfully")
        return cur.lastrowid
   except sqlite3.IntegrityError as e:
       print(f"Could not add album '{name}'. It might already exist. Error: {e}")
       return None

def add_artist(conn, artist_name):
    """
    Create new artist into artists table
    :param conn:
    :param artist_name:
    :return: artist id
    """
    sql = '''INSERT INTO artists(name) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, (artist_name,))
    conn.commit()
    return cur.lastrowid

def add_genre(conn, genre_name):
    """
    Create new genre into genres table
    :param conn:
    :param genre_name:
    :return: genre id
    """
    sql = '''INSERT INTO genres(name) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, (genre_name,))
    conn.commit()
    return cur.lastrowid

# READ / GET OR CREATE
def get_or_create_artist(conn, name):
    """
    Get artist id from artists table. Create a new artist if it does not exist.
    :param conn: Connection object
    :param name: artist name
    :return: artist id
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM artists WHERE name = ?", (name,))
    artist = cur.fetchone()
    if artist is None:
        return add_artist(conn, name)
    return artist[0]

def get_or_create_genre(conn, name):
    """
    Get genre id from genres table. Create a new genre if it does not exist.
    :param conn: Connection object
    :param name: genre name
    :return: genre id
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM genres WHERE name = ?", (name,))
    genre = cur.fetchone()
    if genre is None:
        return add_genre(conn, name)
    return genre[0]

def get_albums_by_genre(conn, genre_name):
    """
    Get all albums by genre.
    :param conn: Connection object
    :param genre_name: name of the genre
    :return: list of albums
    """
    cur = conn.cursor()
    # Using a JOIN to get more readable output
    sql = """SELECT al.name, al.release_date, ar.name, g.name
             FROM albums al
             JOIN artists ar ON al.artist_id = ar.id
             JOIN genres g ON al.genre_id = g.id
             WHERE g.name = ?"""
    cur.execute(sql, (genre_name,))
    return cur.fetchall()

def get_album_by_name(conn, name):
    """
    Get album by name.
    :param conn: Connection object
    :param name: album name
    :return: album tuple or None
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM albums WHERE name = ?", (name,))
    album = cur.fetchone()
    return album
    
# Delete
def delete_album(conn, name):
    """
    Delete an album from the albums table by its name.
    :param conn: Connection object
    :param name: name of the album to delete
    """
    album = get_album_by_name(conn, name)
    if not album:
        print(f"Album '{name}' not found.")
        return

    album_id = album[0]
    sql = "DELETE FROM albums WHERE id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (album_id,))
        conn.commit()
        print(f"Album '{name}' deleted successfully.")
    except Error as e:
        print(e)

# UPDATE
def update_album(conn, name, **kwargs):
    """
    Update album details in the albums table.
    :param conn: Connection object
    :param name: name of the album to update
    :param kwargs: dictionary of columns and new values to update
    """
    album = get_album_by_name(conn, name)
    if not album:
        print(f"Album '{name}' not found.")
        return

    album_id = album[0]
    parameters = [f"{key} = ?" for key in kwargs]
    parameters = ", ".join(parameters)
    values = tuple( v for v in kwargs.values())
    values += (album_id,)
             

    sql = f'''UPDATE albums
            SET {parameters}
            WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print(f"Album '{name}' updated successfully.")
    except sqlite3.OperationalError as e:
       print(f"Error updating album: {e}")