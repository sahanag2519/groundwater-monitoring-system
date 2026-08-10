
import sqlite3


def create_database():

    connection = sqlite3.connect("groundwater.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        village TEXT,
        well TEXT,
        water_level REAL,
        tds INTEGER,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    connection.commit()
    connection.close()


def insert_data(village, well, water_level, tds):

    connection = sqlite3.connect("groundwater.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO sensor_data
    (village, well, water_level, tds)
    VALUES (?, ?, ?, ?)
    """, (village, well, water_level, tds))

    connection.commit()
    connection.close()


create_database()
