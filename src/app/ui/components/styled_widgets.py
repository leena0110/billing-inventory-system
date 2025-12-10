# src/app/ui/components/styled_widgets.py
import tkinter as tk
from ...config.colors import COLORS, FONTS

class StyledButton(tk.Button):
    """Custom styled button class"""
    def __init__(self, master=None, **kwargs):
        # Default style for buttons
        bg = kwargs.pop('bg', COLORS['accent'])
        fg = kwargs.pop('fg', COLORS['text_light'])
        font = kwargs.pop('font', FONTS['normal'])
        relief = kwargs.pop('relief', 'raised')
        bd = kwargs.pop('bd', 1)
        
        super().__init__(master, bg=bg, fg=fg, font=font, 
                        relief=relief, bd=bd, **kwargs)
        
        # Add hover effects
        self.default_bg = bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        if self.default_bg == COLORS['accent']:
            self['bg'] = '#2980b9'  # Darker blue
        elif self.default_bg == COLORS['success']:
            self['bg'] = '#219a52'  # Darker green
        elif self.default_bg == COLORS['danger']:
            self['bg'] = '#c0392b'  # Darker red
    
    def on_leave(self, e):
        self['bg'] = self.default_bg