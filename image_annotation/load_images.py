import sqlite3
import os

conn = sqlite3.connect('annotation_db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS annotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER,
                label TEXT,
                FOREIGN KEY(image_id) REFERENCES images(id))''')
c.execute("DELETE FROM images")
c.execute("DELETE FROM annotations")  # Reset both
conn.commit()
image_dir = 'images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)
    print(f"Created '{image_dir}'. Please add .jpg or .png files.")
    conn.close()
    exit(1)
existing_files = set(os.listdir(image_dir))
for f in sorted(existing_files):
    if f.endswith(('.jpg', '.png')):
        file_path = os.path.join(image_dir, f)
        c.execute("INSERT OR IGNORE INTO images (file_path) VALUES (?)", (file_path,))
conn.commit()
count = c.execute("SELECT COUNT(*) FROM images").fetchone()[0]
conn.close()
print(f"Loaded {count} images")
