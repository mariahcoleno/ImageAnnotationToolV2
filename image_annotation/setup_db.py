import sqlite3

# Connect (creates file if it doesn’t exist)
conn = sqlite3.connect('annotation_db.sqlite')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS annotations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER,
        label TEXT,
        annotated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (image_id) REFERENCES images(id)
    )
''')
conn.commit()
conn.close()
