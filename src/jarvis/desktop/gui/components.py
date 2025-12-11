"""GUI Components Module"""
import tkinter as tk
from tkinter import ttk, scrolledtext


class ConsoleWidget:
    """Console widget for displaying messages"""
    
    def __init__(self, parent):
        self.console = scrolledtext.ScrolledText(
            parent, 
            width=60, 
            height=15, 
            font=('Arial', 12), 
            state=tk.DISABLED, 
            bg='#000000', 
            fg='#ffffff', 
            insertbackground='#ffffff'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
    
    def log(self, message):
        """Log a message to the console"""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear the console"""
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)


class StatusLabel:
    """Status label widget"""
    
    def __init__(self, parent, text="Ready", **kwargs):
        self.status_var = tk.StringVar(value=text)
        self.label = ttk.Label(
            parent, 
            textvariable=self.status_var, 
            font=('Arial', 12), 
            foreground='#ffff00', 
            background='#0a0a1a',
            **kwargs
        )
        self.label.pack(**kwargs)
    
    def update(self, text):
        """Update status text"""
        self.status_var.set(text)


