from pathlib import Path
import sqlite3

DB_PATH = "sample.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    first_time = not Path(DB_PATH).exists()
    conn = get_conn()
    cur = conn.cursor()

    # Simple tasks table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    # Webhook events table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS webhook_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )

    if first_time:
        cur.executemany(
            "INSERT INTO tasks (title, status) VALUES (?, ?)",
            [
                ("Learn FastAPI", "open"),
                ("Build sample backend", "in_progress"),
                ("Show different API styles", "done"),
            ],
        )

    conn.commit()
    conn.close()


def save_chat(room: str, username: str, message: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, username TEXT, message TEXT)"
    )
    cur.execute(
        "INSERT INTO chat_history (room, username, message) VALUES (?, ?, ?)",
        (room, username, message),
    )
    conn.commit()
    conn.close()
