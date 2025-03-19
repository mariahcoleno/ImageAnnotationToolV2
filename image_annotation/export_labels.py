import sqlite3
import csv

conn = sqlite3.connect('annotation_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT file_path, label FROM images JOIN annotations ON images.id = annotations.image_id ORDER BY image_id")
rows = cursor.fetchall()

with open('labeled_images.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_path', 'label'])
    writer.writerows(rows)

print("Exported to labeled_images.csv")
conn.close()
