# modules/arena.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from threading import Thread
from flask import Flask, request
from flask_socketio import SocketIO

class CodingArena(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.server_running = False
        self.setup_ui()
        self.start_server_thread()
    
    def setup_ui(self):
        """Create the user interface"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Problem display
        self.problem_frame = ttk.LabelFrame(self, text="Challenge")
        self.problem_text = scrolledtext.ScrolledText(
            self.problem_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=10
        )
        self.problem_text.pack(expand=True, fill="both")
        
        # Code editor
        self.editor_frame = ttk.LabelFrame(self, text="Your Solution")
        self.code_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            undo=True
        )
        self.code_editor.pack(expand=True, fill="both")
        
        # Controls
        self.control_frame = ttk.Frame(self)
        self.submit_btn = ttk.Button(
            self.control_frame,
            text="Submit Solution",
            command=self.submit_solution
        )
        self.status_label = ttk.Label(
            self.control_frame,
            text="Server: Starting..."
        )
        
        self.submit_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Layout
        self.problem_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.editor_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.control_frame.grid(row=2, column=0, pady=5)
        
        # Load sample problem
        self.load_problem()
    
    def load_problem(self):
        """Load a coding challenge"""
        problem = """Reverse a String:
Write a function that takes a string as input and returns the reversed string.

Example:
Input: "hello"
Output: "olleh"

Constraints:
- Do not use built-in reverse functions
- The solution should be O(n) time complexity
"""
        self.problem_text.config(state=tk.NORMAL)
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(tk.END, problem)
        self.problem_text.config(state=tk.DISABLED)
    
    def submit_solution(self):
        """Submit code for evaluation"""
        code = self.code_editor.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Empty", "Please write some code first!")
            return
        
        if self.server_running:
            messagebox.showinfo("Submitted", "Code submitted to server!")
            # In full implementation, send to WebSocket server
            print(f"Code submitted:\n{code}")
        else:
            messagebox.showerror("Error", "Server not ready yet")
    
    def start_server_thread(self):
        """Start Flask server in background thread"""
        def run_server():
            app = Flask(__name__)
            socketio = SocketIO(app)
            
            @socketio.on('connect')
            def handle_connect():
                print("Client connected")
            
            @app.route('/')
            def home():
                return "STEM Education App - Coding Arena Server"
            
            self.server_running = True
            self.status_label.config(text="Server: Running on port 5000")
            socketio.run(app, port=5000)
        
        Thread(target=run_server, daemon=True).start()