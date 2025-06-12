import sqlite3

def setup_database():
    conn = sqlite3.connect("sarcasm_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_content TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sarcasm_annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_id INTEGER,
            label TEXT,
            annotated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (text_id) REFERENCES texts(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()
    print("Database initialized: sarcasm_db.sqlite")

if __name__ == "__main__":
    setup_database()
