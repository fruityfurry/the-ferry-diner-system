"""
Shortcuts to make tkinter widgets with my particular style options to save on code repetition and clutter.
"""

import tkinter as tk
import colors

class Entry(tk.Entry):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.GUTTER,
                    fg=colors.FOREGROUND,
                    borderwidth=10,
                    relief="flat",
                    highlightbackground=colors.OUTLINE,
                    highlightcolor=colors.HIGHLIGHT,
                    highlightthickness=4,
                    font=("Verdana", 14))