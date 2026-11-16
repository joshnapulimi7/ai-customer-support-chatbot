import sqlite3
from datetime import datetime

DB_NAME = "support_chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            category TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            escalated INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escalated_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            issue_summary TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_chat(session_id, user_message, category, bot_response, escalated=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO chat_logs (session_id, user_message, category, bot_response, escalated, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, user_message, category, bot_response, escalated, now)
    )
    if escalated:
        cursor.execute(
            "INSERT INTO escalated_tickets (session_id, issue_summary, category, status, created_at) VALUES (?, ?, ?, 'Open', ?)",
            (session_id, user_message, category, now)
        )
    conn.commit()
    conn.close()

def get_session_history(session_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_logs WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
