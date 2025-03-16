import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("Script started!")

db_path = '/Users/mariahcoleno/Documents/AnnotationProject/annotation_db.sqlite'
logging.debug(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
logging.debug("Connected to database")
cursor = conn.cursor()
logging.debug("Cursor created")

logging.debug("Fetching unlabeled image")
cursor.execute("SELECT id, file_path FROM images WHERE id NOT IN (SELECT image_id FROM annotations)")
result = cursor.fetchone()
logging.debug(f"Fetched image: {result}")

conn.close()
