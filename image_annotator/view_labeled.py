import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os

def load_labeled_images():
    db_path = 'annotation_db.sqlite'
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found!")
        return []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT i.file_path, a.label FROM images i JOIN annotations a ON i.id = a.image_id")
    images = c.fetchall()
    conn.close()
    print(f"Loaded {len(images)} images from database")
    return images

def main():
    labeled_images = load_labeled_images()
    current_index = [0]

    root = tk.Tk()
    root.title("View Labeled Images")

    image_label = ttk.Label(root)
    image_label.pack(pady=10)

    label_text = ttk.Label(root, text="")
    label_text.pack(pady=5)

    def update_image():
        if labeled_images and current_index[0] < len(labeled_images):
            image_path, label = labeled_images[current_index[0]]
            if os.path.exists(image_path):
                img = Image.open(image_path).resize((300, 300))
                photo = ImageTk.PhotoImage(img)
                image_label.config(image=photo)
                image_label.image = photo
                label_text.config(text=f"Label: {label} ({current_index[0] + 1}/{len(labeled_images)})")
            else:
                label_text.config(text=f"Image not found: {image_path}")
        else:
            label_text.config(text="No labeled images available!")

    def next_image():
        if labeled_images and current_index[0] < len(labeled_images) - 1:
            current_index[0] += 1
            update_image()

    ttk.Button(root, text="Next", command=next_image).pack(pady=5)

    update_image()
    root.mainloop()

if __name__ == "__main__":
    main()
