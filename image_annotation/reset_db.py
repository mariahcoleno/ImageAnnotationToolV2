import sqlite3
conn = sqlite3.connect('annotation_db.sqlite')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS annotations")
c.execute("DROP TABLE IF EXISTS images")
c.execute("CREATE TABLE images (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT)")
c.execute("CREATE TABLE annotations (image_id INTEGER, label TEXT, FOREIGN KEY(image_id) REFERENCES images(id))")
conn.commit()
conn.close()
