# src/app/ui/login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..config.colors import COLORS, FONTS

class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.login_win = tk.Toplevel(app.root)
        self.login_win.title("Login - RITE ELECTRICALS")
        self.login_win.geometry("350x280")
        self.login_win.configure(bg=COLORS['background'])
        self.login_win.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Header
        header_frame = tk.Frame(self.login_win, bg=COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="RITE ELECTRICALS", 
                font=FONTS['title'], fg=COLORS['text_light'], 
                bg=COLORS['primary']).pack(expand=True)
        tk.Label(header_frame, text="Billing System Login", 
                font=FONTS['normal'], fg=COLORS['text_light'], 
                bg=COLORS['primary']).pack(expand=True)
        
        # Main content frame
        content_frame = tk.Frame(self.login_win, bg=COLORS['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Login type selection
        tk.Label(content_frame, text="Login Type:", font=FONTS['header'], 
                bg=COLORS['background'], fg=COLORS['text_dark']).pack(pady=(10, 5))
        self.login_type = tk.StringVar(value="user")
        
        type_frame = tk.Frame(content_frame, bg=COLORS['background'])
        type_frame.pack()
        tk.Radiobutton(type_frame, text="Admin", variable=self.login_type, 
                      value="admin", font=FONTS['normal'], bg=COLORS['background']).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="User", variable=self.login_type, 
                      value="user", font=FONTS['normal'], bg=COLORS['background']).pack(side=tk.LEFT, padx=10)
        
        # Username
        tk.Label(content_frame, text="Username:", font=FONTS['normal'], 
                bg=COLORS['background'], fg=COLORS['text_dark']).pack(pady=(15, 0))
        self.username_entry = tk.Entry(content_frame, font=FONTS['normal'], 
                                     bg=COLORS['light'], relief='solid', bd=1)
        self.username_entry.pack(pady=5, ipady=3)
        
        # Password
        tk.Label(content_frame, text="Password:", font=FONTS['normal'], 
                bg=COLORS['background'], fg=COLORS['text_dark']).pack(pady=(10, 0))
        self.password_entry = tk.Entry(content_frame, show='*', font=FONTS['normal'],
                                     bg=COLORS['light'], relief='solid', bd=1)
        self.password_entry.pack(pady=5, ipady=3)
        
        # Login button
        from .components.styled_widgets import StyledButton
        StyledButton(content_frame, text="Login", command=self.authenticate,
                   bg=COLORS['success'], width=15).pack(pady=15)
        
        self.login_win.grab_set()
    
    def authenticate(self):
        """Authenticate user"""
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        login_type_val = self.login_type.get()
        
        if self.app.authenticate(user, pwd, login_type_val):
            self.login_win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def on_close(self):
        """Handle window close"""
        self.app.root.destroy()
    
    def destroy(self):
        """Destroy login window"""
        self.login_win.destroy()