import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "uploads.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        result TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_upload(filename, result):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO uploads (filename, result, timestamp) VALUES (?, ?, ?)",
              (filename, result, timestamp))

    conn.commit()
    conn.close()

def get_all_uploads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data
