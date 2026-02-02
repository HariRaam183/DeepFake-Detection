import sqlite3
import os
from datetime import datetime
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "uploads.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        created_at TEXT
    )
    """)

    # Uploads table
    c.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        result TEXT,
        timestamp TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

# ========== USER FUNCTIONS ==========

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        hashed = hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
                  (username, email, hashed, created_at))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username or email already exists!"

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = c.fetchone()
    conn.close()
    
    if user:
        return True, user
    return False, None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

# ========== UPLOAD FUNCTIONS ==========

def save_upload(filename, result, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO uploads (filename, result, timestamp, user_id) VALUES (?, ?, ?, ?)",
              (filename, result, timestamp, user_id))

    conn.commit()
    conn.close()

def get_all_uploads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

def get_user_uploads(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads WHERE user_id = ? ORDER BY id DESC", (user_id,))
    data = c.fetchall()
    conn.close()
    return data
