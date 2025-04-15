import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd
import os
from src.process_text import segment_text, suggest_text_emotion

class AnnotatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion and Intent Annotator")
        try:
            self.conn = sqlite3.connect("emotions_intents.sqlite")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
            self.root.destroy()
            return
        self.media_id = None
        self.segments = []
        self.current_segment = 0
        self.label_history = []
        self.setup_gui()

    def setup_gui(self):
        self.upload_btn = tk.Button(self.root, text="Upload Text", command=self.upload_text)
        self.upload_btn.pack(pady=5)
        self.text_area = tk.Text(self.root, height=5, width=50)
        self.text_area.pack(pady=5)
        self.text_area.config(state="disabled")
        self.emotion_label = tk.Label(self.root, text="Emotion:")
        self.emotion_label.pack()
        self.emotion_var = tk.StringVar(value="neutral")
        emotions = ["happy", "sad", "sarcastic", "angry", "neutral"]
        tk.OptionMenu(self.root, self.emotion_var, *emotions).pack()
        self.intent_label = tk.Label(self.root, text="Intent:")
        self.intent_label.pack()
        self.intent_var = tk.StringVar(value="inform")
        intents = ["inform", "persuade", "joke", "complain"]
        tk.OptionMenu(self.root, self.intent_var, *intents).pack()
        tk.Button(self.root, text="Suggest Labels", command=self.suggest_labels).pack(pady=5)
        tk.Button(self.root, text="Save Annotation", command=self.save_labels).pack(pady=5)
        tk.Button(self.root, text="Undo", command=self.undo).pack(pady=5)
        tk.Button(self.root, text="Export CSV", command=self.export_csv).pack(pady=5)

    def upload_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                self.segments = segment_text(content)
                if not self.segments:
                    self.text_area.config(state="normal")
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, "No valid text found.")
                    self.text_area.config(state="disabled")
                    return
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO media (type, content) VALUES (?, ?)",
                    ("text", content)
                )
                self.media_id = cursor.lastrowid
                self.conn.commit()
                self.current_segment = 0
                self.label_history = []
                self.show_segment()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload text: {e}")

    def show_segment(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        if self.current_segment < len(self.segments):
            self.text_area.insert(tk.END, self.segments[self.current_segment])
            self.emotion_var.set("neutral")
            self.intent_var.set("inform")
        else:
            self.text_area.insert(tk.END, "All segments annotated!")
            self.emotion_var.set("neutral")
            self.intent_var.set("inform")
        self.text_area.config(state="disabled")

    def suggest_labels(self):
        if self.current_segment < len(self.segments):
            segment = self.segments[self.current_segment]
            model_emotion = suggest_text_emotion(segment)
            emotion_map = {
                "joy": "happy",
                "sadness": "sad",
                "anger": "angry",
                "neutral": "neutral",
                "disgust": "angry",
                "fear": "sad",
                "surprise": "happy"
            }
            gui_emotion = emotion_map.get(model_emotion.lower(), "neutral")
            if "just kidding" in segment.lower():
                gui_emotion = "sarcastic" if model_emotion in ["joy", "surprise"] else gui_emotion
            self.emotion_var.set(gui_emotion)
            segment_lower = segment.lower()
            if "just kidding" in segment_lower:
                self.intent_var.set("joke")
            elif any(word in segment_lower for word in ["overwhelming", "difficult", "stress"]):
                self.intent_var.set("complain")
            elif gui_emotion in ["happy", "neutral"]:
                self.intent_var.set("inform")
            else:
                self.intent_var.set("complain")

    def save_labels(self):
        if self.current_segment >= len(self.segments):
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO annotations (media_id, segment_id, emotion, intent) VALUES (?, ?, ?, ?)",
                (self.media_id, self.current_segment, self.emotion_var.get(), self.intent_var.get())
            )
            self.conn.commit()
            self.label_history.append((self.current_segment, self.emotion_var.get(), self.intent_var.get()))
            self.current_segment += 1
            self.show_segment()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to save annotation: {e}")

    def undo(self):
        if self.label_history:
            try:
                last = self.label_history.pop()
                cursor = self.conn.cursor()
                cursor.execute(
                    "DELETE FROM annotations WHERE media_id = ? AND segment_id = ?",
                    (self.media_id, last[0])
                )
                self.conn.commit()
                self.current_segment = last[0]
                self.emotion_var.set(last[1])
                self.intent_var.set(last[2])
                self.show_segment()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to undo annotation: {e}")

    def export_csv(self):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT m.id, m.content, a.segment_id, a.emotion, a.intent
                FROM media m
                LEFT JOIN annotations a ON m.id = a.media_id
                WHERE m.type = 'text'
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            if not rows:
                messagebox.showwarning("Warning", "No annotations to export.")
                return
            data = []
            for row in rows:
                media_id, content, segment_id, emotion, intent = row
                if segment_id is not None:
                    segments = segment_text(content)
                    if segment_id < len(segments):
                        data.append({
                            "media_id": media_id,
                            "segment": segments[segment_id],
                            "emotion": emotion or "N/A",
                            "intent": intent or "N/A"
                        })
            if data:
                df = pd.DataFrame(data)
                output_path = os.path.join(os.getcwd(), "annotations_export.csv")
                df.to_csv(output_path, index=False)
                messagebox.showinfo("Success", f"Annotations exported to {output_path}")
            else:
                messagebox.showwarning("Warning", "No valid annotations to export.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotatorGUI(root)
    root.mainloop()
