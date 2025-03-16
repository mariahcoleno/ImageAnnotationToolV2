import sqlite3

# Connect to your database
db_path = '/Users/mariahcoleno/Documents/AnnotationProject/annotation_db.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Count total images in 'images' table
cursor.execute("SELECT COUNT(*) FROM images")
total_images = cursor.fetchone()[0]
print(f"Total images in database: {total_images}")

# Count labeled images in 'annotations' table
cursor.execute("SELECT COUNT(*) FROM annotations")
labeled_images = cursor.fetchone()[0]
print(f"Labeled images: {labeled_images}")

# Breakdown by label
cursor.execute("SELECT label, COUNT(*) FROM annotations GROUP BY label")
label_counts = cursor.fetchall()
print("Label counts:", label_counts)

conn.close()
