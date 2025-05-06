# modules/simulator.py
import tkinter as tk
from tkinter import ttk
from pyopengl.renderer import OpenGLRenderer

class RoboticsSimulator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Create the 3D simulation interface"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Simulation frame
        self.sim_frame = ttk.LabelFrame(self, text="3D Robotics Simulator")
        self.canvas = tk.Canvas(
            self.sim_frame,
            width=800,
            height=600,
            bg="black"
        )
        self.canvas.pack(expand=True, fill="both")
        
        # Controls
        self.control_frame = ttk.Frame(self)
        self.start_btn = ttk.Button(
            self.control_frame,
            text="Start Simulation",
            command=self.start_simulation
        )
        self.reset_btn = ttk.Button(
            self.control_frame,
            text="Reset",
            command=self.reset_simulation
        )
        
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Layout
        self.sim_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.control_frame.grid(row=1, column=0, pady=5)
        
        # Initialize renderer
        self.renderer = OpenGLRenderer(self.canvas.winfo_id())
    
    def start_simulation(self):
        """Start the 3D visualization"""
        self.renderer.start()
    
    def reset_simulation(self):
        """Reset the simulation"""
        self.renderer.reset()