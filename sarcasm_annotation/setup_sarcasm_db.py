import sqlite3

def initialize_db():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    cursor = conn.cursor()

    # Create tables if they don’t exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            text_content TEXT UNIQUE, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sarcasm_annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            text_id INTEGER, 
            label TEXT, 
            annotated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (text_id) REFERENCES texts(id) ON DELETE CASCADE
        )
    ''')

    # Optional: Clear previous annotations and texts
    cursor.execute("DELETE FROM sarcasm_annotations")
    cursor.execute("DELETE FROM texts")  # Remove if you want to keep past data

    conn.commit()
    conn.close()
    print("✅ Sarcasm database initialized and annotations cleared.")

if __name__ == "__main__":
    initialize_db()
