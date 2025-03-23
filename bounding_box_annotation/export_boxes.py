import sqlite3
import csv

def export_annotations():
    conn = sqlite3.connect('bounding_box_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT i.file_path, a.x1, a.y1, a.x2, a.y2, a.label FROM images i JOIN annotations a ON i.id = a.image_id")
    annotations = c.fetchall()
    conn.close()
    
    with open('bounding_boxes.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['file_path', 'x1', 'y1', 'x2', 'y2', 'label'])
        writer.writerows(annotations)

if __name__ == "__main__":
    export_annotations()
