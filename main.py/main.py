# main.py
import tkinter as tk
from tkinter import ttk
from modules.editor import HybridEditor
from modules.arena import CodingArena
from modules.simulator import RoboticsSimulator

class STEMEducationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STEM Education App")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])
        
        # Create notebook interface
        self.notebook = ttk.Notebook(self)
        
        # Initialize modules
        self.editor = HybridEditor(self.notebook)
        self.arena = CodingArena(self.notebook)
        self.simulator = RoboticsSimulator(self.notebook)
        
        # Add tabs
        self.notebook.add(self.editor, text="Code Editor")
        self.notebook.add(self.arena, text="Coding Arena")
        self.notebook.add(self.simulator, text="Robotics Lab")
        
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

if __name__ == "__main__":
    app = STEMEducationApp()
    app.mainloop()