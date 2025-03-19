# view_sarcasm_labels.py
import sqlite3
import tkinter as tk
from tkinter import ttk

db_path = 'sarcasm_db.sqlite'

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT t.text_content, a.label FROM texts t JOIN sarcasm_annotations a ON t.id = a.text_id ORDER BY t.id")
    labeled_texts = cursor.fetchall()

    root = tk.Tk()
    root.title("View Sarcasm Labels")
    root.geometry("400x200")
    text_label = ttk.Label(root, text="", wraplength=350)
    text_label.pack(pady=10)
    index = 0

    def update_display():
        nonlocal index
        if index < len(labeled_texts):
            text_content, label = labeled_texts[index]
            text_label.config(text=f"Text: {text_content}\nLabel: {label} ({index + 1}/{len(labeled_texts)})")
            index += 1
        else:
            root.quit()

    ttk.Button(root, text="Next", command=update_display).pack(pady=20)
    update_display()
    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()
