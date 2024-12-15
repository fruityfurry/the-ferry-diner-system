import tkinter as tk
from tkinter import ttk
from hashlib import sha256 as hash

class Login(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Employee Login")
        self.geometry("800x600")
        
        