import sqlite3
from datetime import datetime


# Create the database and table if it doesn't already exist
def create_db():
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        # Create the attendance table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error while creating the database: {e}")
    finally:
        conn.close()


# Save attendance to the database
def save_attendance(name, timestamp):
    try:
        conn = sqlite3.connect('attendance.db')  # Connect to the database
        cursor = conn.cursor()

        # Insert the attendance record
        cursor.execute("INSERT INTO attendance (name, timestamp) VALUES (?, ?)", (name, timestamp))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving attendance: {e}")
    finally:
        conn.close()


# Fetch all attendance records
def fetch_all_attendance():
    try:
        conn = sqlite3.connect('attendance.db')  # Connect to the database
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance")  # Fetch all rows from the attendance table
        attendance = cursor.fetchall()  # This will return a list of tuples, e.g., [(1, 'Sunayana', '2024-12-19 14:00:00')]

        return attendance

    except sqlite3.Error as e:
        print(f"Error fetching attendance: {e}")
        return []  # Return an empty list in case of error
    finally:
        conn.close()
