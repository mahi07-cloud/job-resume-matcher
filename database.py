import sqlite3
from datetime import datetime

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect("matches.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_desc TEXT,
            resume TEXT,
            score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_match(job_desc, resume, score):
    """Save a match result to the database."""
    conn = sqlite3.connect("matches.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO matches (job_desc, resume, score, timestamp) VALUES (?, ?, ?, ?)",
        (job_desc, resume, score, timestamp)
    )
    conn.commit()
    conn.close()

def get_all_matches():
    """Retrieve all matches from the database."""
    conn = sqlite3.connect("matches.db")
    cursor = conn.cursor()
    cursor.execute("SELECT job_desc, resume, score, timestamp FROM matches")
    results = cursor.fetchall()
    conn.close()
    return results