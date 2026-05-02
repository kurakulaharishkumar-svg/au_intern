import sqlite3
import os

DB_PATH = "internships.db"

def init_db():
    """Initializes the SQLite database and creates the necessary table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_duplicate(link):
    """Checks if a job link has already been sent."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM sent_jobs WHERE link = ?', (link,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_as_sent(link):
    """Marks a job link as sent by storing it in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO sent_jobs (link) VALUES (?)', (link,))
    conn.commit()
    conn.close()
