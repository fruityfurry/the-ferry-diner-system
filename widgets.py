"""
Shortcuts to make tkinter widgets with my particular style options to save on code repetition and clutter.
"""

import tkinter as tk
from tkinter import scrolledtext
import colors

class Label(tk.Label):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.BACKGROUND,
                    fg=colors.FOREGROUND,
                    font=("Verdana", 14))

class Entry(tk.Entry):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.ITEM,
                    fg=colors.FOREGROUND,
                    borderwidth=2,
                    relief="flat",
                    highlightbackground=colors.OUTLINE,
                    highlightcolor=colors.HIGHLIGHT,
                    highlightthickness=2,
                    font=("Verdana", 14))
        
class Button(tk.Button):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.ITEM,
                    fg=colors.FOREGROUND,
                    relief="flat",
                    activebackground=colors.HIGHLIGHT,
                    activeforeground=colors.FOREGROUND,
                    font=("Verdana", 14))
        
class Spinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(readonlybackground=colors.ITEM,
                    fg=colors.FOREGROUND,
                    buttonbackground=colors.ITEM,
                    state="readonly",  # Removes the ability to type into the text box.
                    font=("Verdana", 22))
        
class Dropdown(tk.OptionMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.ITEM,
                    fg=colors.FOREGROUND,
                    borderwidth=2,
                    relief="flat",
                    activebackground=colors.HIGHLIGHT,
                    highlightbackground=colors.OUTLINE,
                    highlightcolor=colors.HIGHLIGHT,
                    highlightthickness=2,
                    width=17,
                    font=("Verdana", 14))
        
class TextBox(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(bg=colors.ITEM,
                    fg=colors.FOREGROUND,
                    relief="flat",
                    highlightbackground=colors.OUTLINE,
                    highlightcolor=colors.OUTLINE,
                    highlightthickness=2,
                    state=tk.DISABLED,
                    font=("Verdana", 14))
        
    def setText(self, text: str) -> None:
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert("1.0", text)
        self.config(state=tk.DISABLED)