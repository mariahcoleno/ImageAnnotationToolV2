import sqlite3

def setup_database():
    conn = sqlite3.connect('bounding_box_db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images 
                 (id INTEGER PRIMARY KEY, file_path TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS annotations 
                 (id INTEGER PRIMARY KEY, image_id INTEGER, x1 INTEGER, y1 INTEGER, 
                  x2 INTEGER, y2 INTEGER, label TEXT, 
                  FOREIGN KEY(image_id) REFERENCES images(id))''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
