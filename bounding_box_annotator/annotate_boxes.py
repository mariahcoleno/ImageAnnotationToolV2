import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import os

class BoundingBoxAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bounding Box Annotator")
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()
        self.images = self.load_images()
        self.current_image_idx = 0
        self.rect_start = None
        self.rect_id = None
        self.label_var = tk.StringVar()
        self.label_entry = tk.Entry(root, textvariable=self.label_var)
        self.label_entry.pack()
        self.save_button = tk.Button(root, text="Save Box", command=self.save_annotation)
        self.save_button.pack()
        self.next_button = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_button.pack()
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)
        self.load_image()

    def load_images(self):
        conn = sqlite3.connect('bounding_box_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT id, file_path FROM images")
        images = c.fetchall()
        conn.close()
        return images

    def load_image(self):
        if self.current_image_idx < len(self.images):
            img_id, img_path = self.images[self.current_image_idx]
            self.current_image_id = img_id
            img = Image.open(img_path).resize((600, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        else:
            self.canvas.create_text(300, 300, text="No more images", font=("Arial", 20))

    def start_rect(self, event):
        self.rect_start = (event.x, event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)

    def draw_rect(self, event):
        if self.rect_start:
            self.canvas.delete(self.rect_id)
            self.rect_id = self.canvas.create_rectangle(
                self.rect_start[0], self.rect_start[1], event.x, event.y, outline="red"
            )

    def end_rect(self, event):
        self.rect_end = (event.x, event.y)

    def save_annotation(self):
        if self.rect_start and self.rect_end and self.label_var.get():
            conn = sqlite3.connect('bounding_box_db.sqlite')
            c = conn.cursor()
            c.execute("INSERT INTO annotations (image_id, x1, y1, x2, y2, label) VALUES (?, ?, ?, ?, ?, ?)",
                      (self.current_image_id, self.rect_start[0], self.rect_start[1],
                       self.rect_end[0], self.rect_end[1], self.label_var.get()))
            conn.commit()
            conn.close()
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.label_var.set("")

    def next_image(self):
        self.current_image_idx += 1
        self.canvas.delete("all")
        self.rect_id = None
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxAnnotator(root)
    root.mainloop()
