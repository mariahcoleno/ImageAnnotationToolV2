import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('annotation_db.sqlite')
c = conn.cursor()

# Ensure the images table exists
c.execute('''CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE)''')
conn.commit()

# Define image directory
image_dir = 'images'

# Check if directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)
    print(f"Created '{image_dir}' directory. Please add .jpg or .png files to proceed.")
    conn.close()
    exit(1)

# Load images, avoiding duplicates
existing_files = set(os.listdir(image_dir))
for f in sorted(existing_files):
    if f.endswith(('.jpg', '.png')):
        file_path = os.path.join(image_dir, f)
        c.execute("INSERT OR IGNORE INTO images (file_path) VALUES (?)", (file_path,))

# Commit changes and get the count
conn.commit()
count = c.execute("SELECT COUNT(*) FROM images").fetchone()[0]
conn.close()

print(f"Loaded {count} images")
