import sqlite3
import os

conn = sqlite3.connect('annotation_db.sqlite')
c = conn.cursor()
image_dir = 'images'
existing_files = set(os.listdir(image_dir))  # Avoid duplicates
for f in sorted(existing_files):
    if f.endswith(('.jpg', '.png')):
        c.execute("INSERT INTO images (file_path) VALUES (?)", (os.path.join(image_dir, f),))
conn.commit()
count = c.execute("SELECT COUNT(*) FROM images").fetchone()[0]  # Query before closing
conn.close()
print("Loaded", count, "images")
