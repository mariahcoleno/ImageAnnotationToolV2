import tkinter as tk
from tkinter import ttk
import sqlite3
import csv

conn = sqlite3.connect('sarcasm_db.sqlite')

def load_messages():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT id, text_content FROM texts ORDER BY id")
    texts = c.fetchall()
    conn.close()
    if not texts:
        return [(1, "Wow, you're SO good at this!"), (2, "I love Mondays."), (3, "Nice weather today.")]
    return texts

def save_label(conn, text_id, label):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO sarcasm_annotations (text_id, label) VALUES (?, ?)", (text_id, label))
    conn.commit()
    print(f"Saved: '{label}' for text_id {text_id}")

def get_labeled_count():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sarcasm_annotations")
    count = c.fetchone()[0]
    conn.close()
    return count

def load_existing_labels():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT t.text_content, a.label FROM sarcasm_annotations a JOIN texts t ON a.text_id = t.id")
    rows = c.fetchall()
    conn.close()
    return rows

def undo_last_label():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    c = conn.cursor()
    c.execute("DELETE FROM sarcasm_annotations WHERE id = (SELECT MAX(id) FROM sarcasm_annotations)")
    conn.commit()
    conn.close()

def export_to_csv():
    conn = sqlite3.connect('sarcasm_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT t.text_content, a.label FROM sarcasm_annotations a JOIN texts t ON a.text_id = t.id")
    rows = c.fetchall()
    conn.close()
    with open('sarcasm_labels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Text', 'Label'])
        writer.writerows(rows)
    print("Exported to sarcasm_labels.csv")

def main():
    messages = load_messages()
    current_index = [0]
    labels = list(load_existing_labels())

    def update_message():
        if current_index[0] < len(messages):
            text_id, text_content = messages[current_index[0]]
            message_label.config(text=text_content)
        else:
            message_label.config(text="All messages labeled!")

    def label_message(label):
        if current_index[0] < len(messages):
            text_id, text_content = messages[current_index[0]]
            if label != "Unsure":
                new_label = "sarcastic" if label == "Sarcastic" else "non-sarcastic"
                save_label(conn, text_id, new_label)
                labels.append((text_content, new_label))
            current_index[0] += 1
            update_message()
            count_label.config(text=f"Labeled: {get_labeled_count()}/{len(messages)}")
            print(f"Labeled: {text_content} -> {label}, Labels={labels}")

    def undo():
        if labels:
            undo_last_label()
            labels.pop()
            if current_index[0] > 0:
                current_index[0] -= 1
            update_message()
            count_label.config(text=f"Labeled: {get_labeled_count()}/{len(messages)}")
            print(f"Undid: Labels={labels}, Index={current_index[0]}")
        else:
            print("Nothing to undo!")

    root = tk.Tk()
    root.title("Sarcasm Annotation")

    message_label = ttk.Label(root, text="", wraplength=400)
    message_label.pack(pady=10)

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=5)

    ttk.Button(button_frame, text="Sarcastic", command=lambda: label_message("Sarcastic")).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Not Sarcastic", command=lambda: label_message("Not Sarcastic")).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Unsure", command=lambda: label_message("Unsure")).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Undo", command=undo).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Export to CSV", command=export_to_csv).pack(side=tk.LEFT, padx=5)

    count_label = ttk.Label(root, text=f"Labeled: {get_labeled_count()}/{len(messages)}")
    count_label.pack(pady=5)

    update_message()
    root.mainloop()

if __name__ == "__main__":
    main()

