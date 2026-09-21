import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

DB_PATH = "nexus_memory.db"

def get_checkpointer():
    """Returns a SQLite checkpointer for short-term session memory."""
    # In a real app, you would reuse the connection, but for simplicity here we use from_conn_string
    return SqliteSaver.from_conn_string(DB_PATH)

def init_long_term_memory():
    """Initialize a simple long-term memory table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            fact TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_fact(user_id: str, fact: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO long_term_memory (user_id, fact) VALUES (?, ?)", (user_id, fact))
    conn.commit()
    conn.close()

def get_facts(user_id: str) -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM long_term_memory WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
