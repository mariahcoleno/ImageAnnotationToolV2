# load_sarcasm_texts.py
import sqlite3

conn = sqlite3.connect('sarcasm_db.sqlite')
cursor = conn.cursor()

# Sample texts (replace with your own if desired)
sample_texts = [
    "Wow, you're *so* good at this game.",
    "I love waiting an hour for my food.",
    "The weather is just perfect today.",
    "Thanks for the help, really appreciate it.",
    "This meeting is definitely worth my time."
]

cursor.execute("DELETE FROM texts")  # Clear previous entries
for text in sample_texts:
    cursor.execute("INSERT OR IGNORE INTO texts (text_content) VALUES (?)", (text,))
conn.commit()

cursor.execute("SELECT COUNT(*) FROM texts")
count = cursor.fetchone()[0]
print(f"Loaded {count} text snippets into the database.")
conn.close()
