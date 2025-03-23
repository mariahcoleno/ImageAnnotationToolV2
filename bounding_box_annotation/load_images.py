import sqlite3
import os

def load_images(image_dir='images'):
    conn = sqlite3.connect('bounding_box_db.sqlite')
    c = conn.cursor()
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg'):
            file_path = os.path.join(image_dir, filename)
            c.execute("INSERT OR IGNORE INTO images (file_path) VALUES (?)", (file_path,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_images()
