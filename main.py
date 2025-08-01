import datetime
import db_operations as db

if __name__ == "__main__":
    database = "database.db"
    albums = [
        ("The Dark Side of the Moon", datetime.date(1973, 3, 1).isoformat(), "Pink Floyd", "Progressive Rock"),
        ("The Wall", datetime.date(1979, 11, 30).isoformat(), "Pink Floyd", "Progressive Rock"),
        ("Abbey Road", datetime.date(1969, 9, 26).isoformat(), "The Beatles", "Rock"),
        ("Hotel California", datetime.date(1976, 11, 21).isoformat(), "Eagles", "Rock"),
        ("Born to Run", datetime.date(1975, 8, 24).isoformat(), "Bruce Springsteen", "Rock"),
        ("Nevermind", datetime.date(1991, 9, 24).isoformat(), "Nirvana", "Grunge"),
        ("Rumours", datetime.date(1977, 12, 20).isoformat(), "Fleetwood Mac", "Soft Rock"),
        ("Back in Black", datetime.date(1976, 7, 25).isoformat(), "AC/DC", "Hard Rock")]
    
    # Create a database connection
    conn = db.create_connection(database)
    if conn:
        try:
            # Setup tables
            db.setup_database(conn)
        except Exception as e:
            print(e)

    # Add albums
    print("\n--- Adding Albums ---")
    album_id = 1
    for album in albums:
        db.add_album(conn, album)

    # Get all Rock albums
    #print("\n--- Rock Albums ---")
    #rock_albums = db.get_albums_by_genre(conn, "Rock")
    #print("Rock albums:")
    #for album in rock_albums:
    #    print(f"  - {album[0]} by {album[2]} ({album[1]})")

    # Remove 'Rumours' album
    #print("\n--- Deleting Album ---")
    #db.delete_album(conn, "Rumours")

    # Update album
    #print("\n--- Updating Album ---")
    #db.update_album(conn, "Back in Black", release_date = datetime.date(1977, 7, 25).isoformat())

    # Close connection
    print("\nClosing database connection.")
    conn.close()

