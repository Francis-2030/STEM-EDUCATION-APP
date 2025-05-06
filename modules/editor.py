# modules/editor.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class HybridEditor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Blockly workspace simulation
        self.blockly_frame = ttk.LabelFrame(self, text="Visual Programming")
        self.blockly_canvas = tk.Canvas(self.blockly_frame, bg="#ffffff")
        self.blockly_canvas.pack(expand=True, fill="both")
        
        # Python editor
        self.code_frame = ttk.LabelFrame(self, text="Python Code")
        self.code_editor = scrolledtext.ScrolledText(
            self.code_frame, 
            wrap=tk.WORD,
            font=("Consolas", 11),
            undo=True
        )
        self.code_editor.pack(expand=True, fill="both")
        
        # Controls
        self.control_frame = ttk.Frame(self)
        self.convert_btn = ttk.Button(
            self.control_frame,
            text="Generate Python",
            command=self.generate_python
        )
        self.run_btn = ttk.Button(
            self.control_frame,
            text="Run Code",
            command=self.run_code
        )
        
        self.convert_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Layout
        self.blockly_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.code_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.control_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Load sample blocks
        self.load_sample_blocks()
    
    def load_sample_blocks(self):
        """Visual representation of blocks"""
        colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335"]
        for i, color in enumerate(colors):
            x1, y1 = 50, 50 + i*70
            x2, y2 = 200, 100 + i*70
            self.blockly_canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="block")
            self.blockly_canvas.create_text((x1+x2)/2, (y1+y2)/2, 
                                          text=f"Block {i+1}", 
                                          fill="white")
    
    def generate_python(self):
        """Convert visual blocks to Python"""
        sample_code = """# Generated from blocks
def greet():
    print("Hello from STEM App!")
    
greet()"""
        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(tk.END, sample_code)
    
    def run_code(self):
        """Execute the Python code"""
        code = self.code_editor.get(1.0, tk.END)
        try:
            exec(code, {})
            messagebox.showinfo("Success", "Code executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed:\n{str(e)}")