import tkinter as tk
from tkinter import ttk
import sqlite3
import csv

def setup_database():
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS labels
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message TEXT,
                  label TEXT)''')
    # Clear existing data to start fresh each run (optional: comment out if you want persistence)
    c.execute("DELETE FROM labels")
    conn.commit()
    conn.close()

def load_messages():
    return ["Wow, you're SO good at this!", "I love Mondays.", "Nice weather today."]

def save_label(message, label):
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute("INSERT INTO labels (message, label) VALUES (?, ?)", (message, label))
    conn.commit()
    conn.close()

def get_labeled_count():
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM labels")
    count = c.fetchone()[0]
    conn.close()
    return count

def load_existing_labels():
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute("SELECT message, label FROM labels")
    rows = c.fetchall()
    conn.close()
    return rows

def undo_last_label():
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute("DELETE FROM labels WHERE id = (SELECT MAX(id) FROM labels)")
    conn.commit()
    conn.close()

def export_to_csv():
    conn = sqlite3.connect('sarcasm_labels.db')
    c = conn.cursor()
    c.execute("SELECT message, label FROM labels")
    rows = c.fetchall()
    conn.close()
    with open('sarcasm_labels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Message', 'Label'])
        writer.writerows(rows)
    print("Exported to sarcasm_labels.csv")

def main():
    setup_database()
    messages = load_messages()
    current_index = [0]
    labels = list(load_existing_labels())  # Load existing labels from DB

    def update_message():
        if current_index[0] < len(messages):
            message_label.config(text=messages[current_index[0]])
        else:
            message_label.config(text="All messages labeled!")

    def label_message(label):
        if current_index[0] < len(messages):
            message = messages[current_index[0]]
            save_label(message, label)
            labels.append((message, label))
            current_index[0] += 1
            update_message()
            count_label.config(text=f"Labeled: {get_labeled_count()}/{len(messages)}")
            print(f"Labeled: {message} -> {label}, Labels={labels}")

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
