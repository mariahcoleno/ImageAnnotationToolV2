import sqlite3

conn = sqlite3.connect('sarcasm_db.sqlite')
cursor = conn.cursor()

# Create tables if they don’t exist
cursor.execute('''CREATE TABLE IF NOT EXISTS texts (id INTEGER PRIMARY KEY AUTOINCREMENT, text_content TEXT UNIQUE, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS sarcasm_annotations (id INTEGER PRIMARY KEY AUTOINCREMENT, text_id INTEGER, label TEXT, annotated_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (text_id) REFERENCES texts(id))''')

# Clear annotations (optional: comment out to preserve)
cursor.execute("DELETE FROM sarcasm_annotations")
conn.commit()

conn.close()
print("Sarcasm database initialized and annotations cleared.")
