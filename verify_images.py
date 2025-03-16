import sqlite3
import os

db_path = '/Users/mariahcoleno/Documents/AnnotationProject/annotation_db.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM images")
print(f"Images in database: {cursor.fetchone()[0]}")

cursor.execute("SELECT file_path FROM images LIMIT 5")
print("Sample paths:", cursor.fetchall())
conn.close()
