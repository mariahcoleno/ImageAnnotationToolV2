import sqlite3

def setup_db(db_path="emotions_intents.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Media table: stores text/audio/video inputs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    
    # Annotations table: stores emotion/intent labels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id INTEGER NOT NULL,
            segment_id INTEGER NOT NULL,
            emotion TEXT,
            intent TEXT,
            annotated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (media_id) REFERENCES media(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    setup_db()
