import sqlite3
import os

db_path = 'annotation_db.sqlite'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear existing entries (fresh start)
cursor.execute("DELETE FROM images")
conn.commit()

image_dir = os.path.expanduser('~/Documents/AnnotationProject/images')
for img_file in os.listdir(image_dir):
    if img_file.endswith('.jpg'):  # Only load .jpg files
        file_path = os.path.join(image_dir, img_file)
        cursor.execute("INSERT OR IGNORE INTO images (file_path) VALUES (?)", (file_path,))
conn.commit()

cursor.execute("SELECT COUNT(*) FROM images")
print(f"Loaded {cursor.fetchone()[0]} images")
conn.close()
