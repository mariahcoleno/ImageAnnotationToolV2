import sqlite3

# Connect to the database
conn = sqlite3.connect('sarcasm_labels.db')
c = conn.cursor()

# Drop existing tables if they exist
c.execute("DROP TABLE IF EXISTS annotations")
c.execute("DROP TABLE IF EXISTS texts")

# Create tables
c.execute("CREATE TABLE texts (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
c.execute("CREATE TABLE annotations (text_id INTEGER, label TEXT, FOREIGN KEY(text_id) REFERENCES texts(id))")

# Commit changes and close
conn.commit()
conn.close()
