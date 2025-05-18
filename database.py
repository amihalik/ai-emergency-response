import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "emergency.db"


def get_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)


def init_db(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            capacity INTEGER NOT NULL,
            availability INTEGER NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            assigned_resource_id INTEGER,
            eta_minutes REAL,
            FOREIGN KEY(assigned_resource_id) REFERENCES resources(id)
        )
        """
    )
    conn.commit()


def seed_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM resources")
    if cur.fetchone()[0] > 0:
        return
    resources = [
        ("fire", "Station 1", 40.7128, -74.0060, 5, 5),
        ("fire", "Station 2", 40.7308, -73.9975, 3, 3),
        ("hospital", "City Hospital", 40.7139, -74.0039, 10, 10),
        ("hospital", "Metro Hospital", 40.7340, -74.0020, 8, 8),
        ("police", "Precinct 1", 40.7150, -74.0090, 6, 6),
        ("police", "Precinct 2", 40.7315, -73.9900, 4, 4),
    ]
    cur.executemany(
        """
        INSERT INTO resources (type, name, latitude, longitude, capacity, availability)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        resources,
    )
    conn.commit()

