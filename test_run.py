import sys
import os

# Add the src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from app.billing_app import BillingApp
    import tkinter as tk
    
    print("🚀 LAUNCHING RITE ELECTRICALS APPLICATION...")
    print("=" * 50)
    print("This will open the FULL application with login screen")
    print("Please login with:")
    print("  Admin: admin/admin123")
    print("  User: user/user123")
    print("=" * 50)
    
    # Create the main window
    root = tk.Tk()
    
    # Create the application (this shows login window)
    app = BillingApp(root)
    
    print("✅ Application initialized!")
    print("✅ Login window should be visible")
    print("✅ After login, main window will appear")
    
    # Start the main loop
    root.mainloop()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")