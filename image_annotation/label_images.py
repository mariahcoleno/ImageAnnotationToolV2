# label_images.py
import sqlite3
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("Script started!")

db_path = 'annotation_db.sqlite'

def get_unlabeled_image(cursor):
    cursor.execute("SELECT id, file_path FROM images WHERE id NOT IN (SELECT image_id FROM annotations)")
    result = cursor.fetchone()
    logging.debug(f"Fetched unlabeled image: {result}")
    return result

def save_label(cursor, conn, image_id, label):
    cursor.execute("INSERT INTO annotations (image_id, label) VALUES (?, ?)", (image_id, label))
    conn.commit()
    logging.debug(f"Saved label: {label} for image_id: {image_id}")

def main():
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        # Initialize labeled_count from database
        cursor.execute("SELECT COUNT(*) FROM annotations")
        labeled_count = cursor.fetchone()[0]
        logging.debug(f"Starting with {labeled_count} labeled images")

        root = tk.Tk()
        root.title("Image Annotation Tool")
        root.geometry("400x400")
        img_label = ttk.Label(root)
        img_label.pack()
        counter_label = ttk.Label(root, text=f"Labeled: {labeled_count}/100")
        counter_label.pack()

        def update_counter():
            nonlocal labeled_count
            labeled_count += 1
            counter_label.config(text=f"Labeled: {labeled_count}/100")
            logging.debug(f"Counter updated to {labeled_count}")

        def update_image():
            img_data = get_unlabeled_image(cursor)
            if img_data:
                image_id, file_path = img_data
                logging.debug(f"Loading image: {file_path} (id: {image_id})")
                img = Image.open(file_path).resize((300, 300), Image.Resampling.LANCZOS)
                logging.debug(f"Resized image size: {img.size}")
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                img_label.image = photo  # Keep reference to avoid garbage collection
                root.update()
                logging.debug("Image set")
                return image_id
            else:
                logging.debug("All images labeled!")
                counter_label.config(text=f"Labeled: {labeled_count}/100 - Done!")
                root.quit()
                return None

        image_id = update_image()
        if image_id is None:
            root.quit()
        else:
            def on_label(label):
                nonlocal image_id
                if image_id:
                    save_label(cursor, conn, image_id, label)
                    update_counter()
                    image_id = update_image()

            ttk.Button(root, text="Cat", command=lambda: on_label("cat")).pack(side=tk.LEFT, padx=10)
            ttk.Button(root, text="Dog", command=lambda: on_label("dog")).pack(side=tk.RIGHT, padx=10)

        root.mainloop()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
