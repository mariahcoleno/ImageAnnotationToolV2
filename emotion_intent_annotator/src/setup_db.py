import sqlite3

def setup_database():
    try:
        conn = sqlite3.connect("emotions_intents.sqlite")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                filename TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS annotations (
                media_id INTEGER,
                segment_id INTEGER,
                emotion TEXT,
                intent TEXT,
                PRIMARY KEY (media_id, segment_id),
                FOREIGN KEY (media_id) REFERENCES media(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edits (
                media_id INTEGER,
                segment_id INTEGER,
                old_text TEXT,
                new_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (media_id) REFERENCES media(id)
            )
        """)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database setup failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
