import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

SAMPLE_HYPOTHESES = [
    ("Increased CO2 accelerates plant growth", "text"),
    ("images/ssc2019-15b-med.jpg", "image", "This galaxy cluster shows gravitational lensing"),
    ("Quantum entanglement enables faster-than-light communication", "text")
]

conn = sqlite3.connect('hypotheses.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS hypotheses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   data TEXT,
                   modality TEXT,
                   label TEXT,
                   hypothesis TEXT)''')
cursor.executemany("INSERT INTO hypotheses (data, modality, hypothesis) SELECT ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM hypotheses WHERE data = ?)", 
                  [(h[0], h[1], h[2] if len(h) > 2 else h[0], h[0]) for h in SAMPLE_HYPOTHESES])
conn.commit()

class HypothesisAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hypothesis Annotator")
        self.entries = self.load_entries()
        self.current_idx = 0
        self.image_refs = []

        self.label_frame = tk.Frame(root)
        self.label_frame.pack(pady=10)
        self.label_text = tk.Label(self.label_frame, text="", wraplength=400)
        self.label_text.pack()
        self.label_image = tk.Label(self.label_frame)
        self.label_image.pack()

        self.progress = tk.Label(root, text=f"Labeled: 0/{len(self.entries)}")
        self.progress.pack()

        for label in ["Supported", "Refuted", "Unsure"]:
            tk.Button(root, text=label, command=lambda l=label: self.annotate(l)).pack(side=tk.LEFT, padx=5)

        tk.Button(root, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Export to CSV", command=self.export).pack(side=tk.RIGHT, padx=5)

        self.show_current()

    def load_entries(self):
        return cursor.execute("SELECT id, data, modality, label, hypothesis FROM hypotheses").fetchall()

    def show_current(self):
        entry = self.entries[self.current_idx]
        if entry[2] == "image":
            self.label_text.config(text=entry[4])
            try:
                img = Image.open(entry[1]).resize((300, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.label_image.config(image=photo)
                self.image_refs.append(photo)
            except Exception as e:
                self.label_image.config(image="")
                print(f"Image load error: {e}")
        else:
            self.label_text.config(text=entry[4])
            self.label_image.config(image="")
        self.update_progress()

    def annotate(self, label):
        entry = self.entries[self.current_idx]
        cursor.execute("UPDATE hypotheses SET label = ? WHERE id = ?", (label, int(entry[0])))
        conn.commit()
        self.entries = self.load_entries()
        self.next_entry()

    def next_entry(self):
        self.current_idx += 1
        if self.current_idx < len(self.entries):
            self.show_current()
        else:
            messagebox.showinfo("Done", "All hypotheses labeled! Export your data or adjust labels.")
            self.current_idx -= 1

    def undo(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            entry = self.entries[self.current_idx]
            cursor.execute("UPDATE hypotheses SET label = NULL WHERE id = ?", (int(entry[0]),))
            conn.commit()
            self.entries = self.load_entries()
            self.show_current()
        else:
            print("Undo blocked: idx=0")

    def update_progress(self):
        labeled = sum(1 for e in self.entries if e[3] is not None)
        self.progress.config(text=f"Labeled: {labeled}/{len(self.entries)}")

    def export(self):
        with open('hypothesis_data.csv', 'w') as f:
            f.write("id,data,modality,label,hypothesis\n")
            for entry in self.entries:
                label = entry[3] if entry[3] is not None else "Unlabeled"
                f.write(f"{entry[0]},\"{entry[1]}\",\"{entry[2]}\",\"{label}\",\"{entry[4]}\"\n")
        messagebox.showinfo("Export", "Saved to hypothesis_data.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = HypothesisAnnotator(root)
    root.mainloop()
    conn.close()
