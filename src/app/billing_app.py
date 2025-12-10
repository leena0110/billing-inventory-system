import tkinter as tk
from datetime import datetime

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RITE ELECTRICALS - Billing System")
        self.root.geometry("1000x700")
        
        # Import here to avoid circular import
        try:
            from .config.colors import COLORS, FONTS
        except ImportError:
            # Fallback if import fails
            COLORS = {
                'primary': '#2c3e50', 'secondary': '#34495e', 'accent': '#3498db',
                'success': '#27ae60', 'warning': '#f39c12', 'danger': '#e74c3c',
                'light': '#ecf0f1', 'dark': '#2c3e50', 'background': '#f8f9fa',
                'header': '#ffffff', 'text_light': '#ffffff', 'text_dark': '#2c3e50'
            }
            FONTS = {
                'title': ('Arial', 16, 'bold'), 'header': ('Arial', 12, 'bold'),
                'normal': ('Arial', 10), 'small': ('Arial', 9)
            }
        
        # Set colors and fonts as instance variables
        self.COLORS = COLORS
        self.FONTS = FONTS
        
        # Set icon if available
        self.set_icon()
        
        self.root.withdraw()  # Hide main window initially
        
        # Company details
        self.company = {
            "name": "RITE ELECTRICALS",
            "address": "451A, Periyar Nagar, Opp Rajaji Statue\nThirumangalam-625 706\nMadurai Main Road, Tamil Nadu",
            "phone": "9342244061 , 9842204841",
            "gstin": "GSTIN: 33BMGPM7077J1ZO"
        }
        
        # Variables
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.bill_no = tk.StringVar()
        self.current_date = tk.StringVar()
        self.bill_type = tk.StringVar(value="R")
        self.search_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.products = []
        self.bill_items = []
        self.user_role = None
        self.place_var = tk.StringVar()
        self.site_var = tk.StringVar()
        self.payment_type = tk.StringVar(value="Cash")
        self.include_gst = tk.BooleanVar(value=False)
        self.amount_paid_var = tk.StringVar()
        self.remaining_amount_var = tk.StringVar()
        
        # Initialize modules - import here to avoid circular imports
        from .billing_operations import BillingOperations
        from .product_operations import ProductOperations
        from .admin_features import AdminFeatures
        
        self.billing_ops = BillingOperations(self)
        self.product_ops = ProductOperations(self)
        self.admin_features = AdminFeatures(self)
        
        # Load data and show login
        self.load_products()
        self.show_login()
        self.update_date()
    
    def set_icon(self):
        """Set application icon"""
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            try:
                import os
                icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "favicon.ico")
                self.root.iconbitmap(icon_path)
            except:
                print("Icon file not found, running without icon")
    
    def on_close(self):
        """Handle window close event"""
        self.root.destroy()
    
    def show_login(self):
        """Show the login window"""
        from .ui.login_window import LoginWindow
        self.login_ui = LoginWindow(self)
    
    def setup_admin_menu(self):
        """Setup admin menu features"""
        if self.user_role == "admin":
            self.admin_features.setup_admin_features()
    
    def setup_ui(self):
        """Setup the main UI"""
        from .ui.main_window import MainWindow
        self.main_ui = MainWindow(self.root, self)
    
    def load_products(self):
        """Load products from file"""
        from .models.product import ProductModel
        self.products = ProductModel.load_products()
    
    def update_date(self):
        """Update current date and check for rate changes"""
        self.current_date.set(datetime.now().strftime("%d/%m/%Y %I:%M %p"))
        
        # Check for future rate changes every minute
        self.product_ops.check_and_apply_future_rate_changes()
        
        self.root.after(60000, self.update_date)
    
    # Delegate methods to modules
    def save_bill(self):
        """Save current bill"""
        return self.billing_ops.save_bill()
    
    def generate_and_set_bill_number(self):
        """Generate bill number"""
        return self.billing_ops.generate_and_set_bill_number()
    
    def get_current_product_stock(self, brand, product_name):
        """Get current stock for a product"""
        return self.product_ops.get_current_product_stock(brand, product_name)
    
    def get_current_rate_for_product(self, product_name, current_date=None):
        """Get current rate for a product"""
        return self.product_ops.get_current_rate_for_product(product_name, current_date)


