# test_gui.py
import tkinter as tk
root = tk.Tk()
root.title("Test GUI")
tk.Label(root, text="Test Label").pack()
tk.Button(root, text="Test Button").pack()
root.mainloop()
