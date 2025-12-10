# main.py
import tkinter as tk
from src.app.billing_app import BillingApp

if __name__ == "__main__":
    try:
        print("Starting RITE ELECTRICALS Billing System...")
        root = tk.Tk()
        app = BillingApp(root)
        print("Application started successfully!")
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")