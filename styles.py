"""
Defines the styles that will be used for the various widgets throughout this project to save on code repitition and aid
in code maintainability and ease of editing.
"""

import tkinter as tk
from tkinter import ttk
import colors

def entryStyle(master: tk.Tk) -> None:
    """
    Defines style of ttk.Entry.
    """
    
    style = ttk.Style(master)
    style.configure("TEntry",
                    font=("Verdana", 22),
                    background=colors.GUTTER,
                    foreground=colors.FOREGROUND,
                    highlightbackground="#00ffff")
    style.layout("TEntry", [
        ("Entry.background", colors.GUTTER)
    ])
    
def defineAllStyles(master: tk.Tk) -> None:
    """
    Defines all styles at once for given root window.
    """
    entryStyle(master)