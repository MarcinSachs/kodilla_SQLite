# kodilla_SQLite

## Project Description

This project is a simple Python application designed to manage a collection of music albums using an SQLite database. The application demonstrates basic CRUD (Create, Read, Update, Delete) operations on data such as albums, artists, and music genres.

## Features

*   **Database Connection:** Establishes a connection to the SQLite database file.
*   **Database Setup:** Creates the necessary tables (`artists`, `genres`, `albums`) if they do not already exist.
*   **Adding Albums:** Allows adding new albums, automatically creating new artists and genres if they don't yet exist in the database.
*   **Retrieving Albums:** Examples of fetching albums, e.g., by genre.
*   **Updating Albums:** Modifying data for existing albums.
*   **Deleting Albums:** Removing albums from the database.
*   **Error Handling:** Basic error handling for `sqlite3.Error` and `sqlite3.IntegrityError` for database operations.

## Requirements

*   Python 3.x
*   Standard Python modules: `sqlite3`, `datetime` (no `pip` installation required).

## Project Structure

*   `main.py`: The main application script. It contains the logic for initializing the database, adding sample data, and demonstrating the use of CRUD functions from the `db_operations` module. You can uncomment/comment sections here to test different operations.
*   `db_operations.py`: A module containing all functions responsible for interacting with the database, such as creating connections, setting up tables, and performing all CRUD operations on albums, artists, and genres.
*   `database.db`: The SQLite database file. It will be automatically created in the same directory as the scripts upon the first run of `main.py`.

## Installation and Running

1.  **Download Files:** Ensure you have `main.py` and `db_operations.py` in the same directory.
2.  **Run the Script:** Open your terminal or command prompt, navigate to the directory where the files are located, and run the script:
    ```bash
    python main.py
    ```
3.  **Database:** The `database.db` file will be automatically created, and the tables will be initialized. The script will perform the sample operations (adding, deleting, updating) that are uncommented in `main.py`.

## Usage

In the `main.py` file, you will find demonstration sections for each operation (adding, retrieving, deleting, updating). You can uncomment (`#` at the beginning of the line) or comment out these sections to test specific functionalities.

Example usage of the `update_album` function:

```python
# main.py
# ...
    print("\n--- Updating Album ---")
    db.update_album(conn, "Back in Black", release_date = datetime.date(1977, 7, 25).isoformat())
# ...