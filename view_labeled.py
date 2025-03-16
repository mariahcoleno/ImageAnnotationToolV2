import sqlite3
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

db_path = '/Users/mariahcoleno/Documents/AnnotationProject/annotation_db.sqlite'

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path, label FROM images JOIN annotations ON images.id = annotations.image_id ORDER BY image_id")
    labeled_images = cursor.fetchall()

    root = tk.Tk()
    root.title("View Labeled Images")
    root.geometry("400x450")

    img_label = ttk.Label(root)
    img_label.pack()
    text_label = ttk.Label(root, text="")
    text_label.pack()
    index = 0

    def update_display():
        nonlocal index
        if index < len(labeled_images):
            file_path, label = labeled_images[index]
            img = Image.open(file_path)
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo)
            img_label.image = photo
            text_label.config(text=f"Image: {file_path.split('/')[-1]} | Label: {label} | {index + 1}/{len(labeled_images)}")
            index += 1
        else:
            root.quit()

    ttk.Button(root, text="Next", command=update_display).pack()
    update_display()  # Show first image
    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()
