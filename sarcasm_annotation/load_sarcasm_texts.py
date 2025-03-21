# load_sarcasm_texts.py
import sqlite3

conn = sqlite3.connect('sarcasm_db.sqlite')
cursor = conn.cursor()

cursor.execute("DELETE FROM texts")  # Clear previous entries
with open('texts.txt', 'r') as f:
    texts = [line.strip() for line in f if line.strip()]
for text in texts:
    cursor.execute("INSERT OR IGNORE INTO texts (text_content) VALUES (?)", (text,))
conn.commit()

cursor.execute("SELECT COUNT(*) FROM texts")
count = cursor.fetchone()[0]
print(f"Loaded {count} text snippets from texts.txt")
conn.close()
