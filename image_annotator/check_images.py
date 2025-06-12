import sqlite3
import os

db_path = 'annotation_db.sqlite'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM images")
print(f"Images in database: {cursor.fetchone()[0]}")

cursor.execute("SELECT file_path FROM images")
paths = cursor.fetchall()
for path in paths:
    print(path[0])
conn.close()

