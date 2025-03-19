import sqlite3
import tkinter as tk
from tkinter import ttk
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("Script started!")

db_path = 'sarcasm_db.sqlite'

def get_unlabeled_text(cursor):
    cursor.execute("SELECT id, text_content FROM texts WHERE id NOT IN (SELECT text_id FROM sarcasm_annotations)")
    return cursor.fetchone()

def save_label(cursor, conn, text_id, label):
    cursor.execute("INSERT INTO sarcasm_annotations (text_id, label) VALUES (?, ?)", (text_id, label))
    conn.commit()
    logging.debug(f"Saved label: {label} for text_id: {text_id}")

def main():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sarcasm_annotations")
    labeled_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM texts")
    total_count = cursor.fetchone()[0]

    root = tk.Tk()
    root.title("Sarcasm Annotation Tool")
    root.geometry("400x200")

    # Text and counter labels
    text_label = ttk.Label(root, text="", wraplength=350)
    text_label.pack(pady=10)
    counter_label = ttk.Label(root, text=f"Labeled: {labeled_count}/{total_count}")
    counter_label.pack()

    # Frame for buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    last_text_id = None

    def update_counter(increment=True):
        nonlocal labeled_count
        if increment:
            labeled_count += 1
        else:
            labeled_count -= 1
        counter_label.config(text=f"Labeled: {labeled_count}/{total_count}")

    def update_text():
        nonlocal last_text_id
        text_data = get_unlabeled_text(cursor)
        if text_data:
            text_id, text_content = text_data
            text_label.config(text=text_content)
            last_text_id = text_id
            return text_id
        else:
            text_label.config(text="All texts labeled!")
            counter_label.config(text=f"Labeled: {labeled_count}/{total_count} - Done!")
            for widget in button_frame.winfo_children():
                widget.config(state='disabled')
            return None

    def undo():
        nonlocal last_text_id
        if last_text_id and labeled_count > 0:
            cursor.execute("DELETE FROM sarcasm_annotations WHERE text_id = ? AND annotated_at = (SELECT MAX(annotated_at) FROM sarcasm_annotations WHERE text_id = ?)", (last_text_id, last_text_id))
            conn.commit()
            update_counter(increment=False)
            last_text_id = update_text()

    text_id = update_text()
    if text_id is not None:
        def on_label(label):
            nonlocal text_id
            if text_id:
                save_label(cursor, conn, text_id, label)
                update_counter()
                text_id = update_text()

        # Buttons in frame, side by side
        ttk.Button(button_frame, text="Sarcastic", command=lambda: on_label("sarcastic")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Maybe", command=lambda: on_label("maybe")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Not Sarcastic", command=lambda: on_label("not_sarcastic")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Undo", command=undo).pack(side=tk.LEFT, padx=5)

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()
