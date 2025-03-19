# export_sarcasm_labels.py
import sqlite3
import csv

conn = sqlite3.connect('sarcasm_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT t.text_content, a.label FROM texts t JOIN sarcasm_annotations a ON t.id = a.text_id")
rows = cursor.fetchall()

with open('sarcasm_labels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'label'])
    writer.writerows(rows)
conn.close()
print("Annotations exported to sarcasm_labels.csv")
