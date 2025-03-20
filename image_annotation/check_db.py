import sqlite3
import os

db_path = os.path.expanduser('~/Documents/AnnotationProject/image_annotation/ annotation_db.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables in database:", cursor.fetchall())
conn.close()

