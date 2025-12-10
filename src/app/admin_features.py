# src/app/admin_features.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
from tkcalendar import DateEntry

class AdminFeatures:
    """Admin-only features for the application"""
    
    def __init__(self, app):
        self.app = app
        print("✅ AdminFeatures initialized")
    
    def setup_admin_features(self):
        """Setup admin menu features"""
        print("🔄 Setting up admin menu...")
        menubar = tk.Menu(self.app.root)
        
        # Sales Entry menu
        sales_menu = tk.Menu(menubar, tearoff=0)
        sales_menu.add_command(label="Add Product", command=self.add_product_window)
        sales_menu.add_command(label="View Products", command=self.view_products)
        sales_menu.add_command(label="Rate Change", command=self.rate_change_window)
        sales_menu.add_command(label="Add Sales Receipt", command=self.sales_receipt_window)
        menubar.add_cascade(label="Sales Entry", menu=sales_menu)
        
        # Customers menu
        customers_menu = tk.Menu(menubar, tearoff=0)
        customers_menu.add_command(label="View Customers", command=self.view_customers)
        menubar.add_cascade(label="Customers", menu=customers_menu)
        
        # Purchases menu
        purchases_menu = tk.Menu(menubar, tearoff=0)
        purchases_menu.add_command(label="Purchase Entry", command=self.purchase_entry_window)
        purchases_menu.add_command(label="View Purchases", command=self.view_purchases)
        purchases_menu.add_command(label="Add Purchase Receipt", command=self.purchase_receipt_window)
        menubar.add_cascade(label="Purchases", menu=purchases_menu)
        
        # Summary menu
        summary_menu = tk.Menu(menubar, tearoff=0)
        summary_menu.add_command(label="Stock Summary", command=self.view_stocks)
        summary_menu.add_command(label="Purchase Receipt Summary", command=self.view_purchase_receipts)
        summary_menu.add_command(label="Sales Receipt Summary", command=self.view_sales_receipts)
        menubar.add_cascade(label="Summary", menu=summary_menu)
        
        # Sales Report menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        reports_menu.add_command(label="Daily Report", command=lambda: self.generate_sales_report("daily"))
        reports_menu.add_command(label="Fortnight Report", command=lambda: self.generate_sales_report("fortnight"))
        reports_menu.add_command(label="Monthly Report", command=lambda: self.generate_sales_report("monthly"))
        reports_menu.add_command(label="Custom Date Report", command=lambda: self.generate_sales_report("custom"))
        menubar.add_cascade(label="Sales Report", menu=reports_menu)
        
        self.app.root.config(menu=menubar)
        print("✅ Admin menu setup complete")
    
    # Add this method to get brands
    def get_brands(self):
        """Get unique brands from products"""
        return sorted(set(p.get("Brand", "") for p in self.app.products))
    
    # Add this method to load customers
    def _load_customers(self):
        """Load customers from CSV file"""
        if not os.path.exists("customers.csv"):
            return []
            
        customers = []
        try:
            with open("customers.csv", mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customers.append({
                        "Name": row.get("Name", ""),
                        "Phone": row.get("Phone", ""),
                        "Place": row.get("Place", ""),
                        "Site": row.get("Site", "")
                    })
        except Exception as e:
            print(f"Error loading customers: {str(e)}")
        return customers
    
    def add_product_window(self):
        """Open add product window - FULL implementation"""
        print("📝 Opening Add Product Window...")
        
        add_window = tk.Toplevel(self.app.root)
        add_window.title("Add Product")
        add_window.geometry("600x700")
        
        # Store reference
        self.current_add_window = add_window
        
        # Create entry widgets
        tk.Label(add_window, text="Brand Name:").pack()
        brand_entry = ttk.Combobox(add_window, values=self.get_brands(), width=30)
        brand_entry.pack()
        
        tk.Label(add_window, text="Product Name:").pack()
        name_entry = ttk.Combobox(add_window, width=30)
        name_entry.pack()
        
        tk.Label(add_window, text="Purchase Date:").pack()
        date_entry = DateEntry(add_window, width=12, background='darkblue', 
                            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.pack()
        
        tk.Label(add_window, text="Purchase Rate:").pack()
        purchase_entry = tk.Entry(add_window)
        purchase_entry.pack()
        
        tk.Label(add_window, text="Margin1 (%):").pack()
        margin1_entry = tk.Entry(add_window)
        margin1_entry.pack()
        
        # Wholesale rate entry
        wholesale_rate_var = tk.StringVar()
        tk.Label(add_window, text="Wholesale Rate:").pack()
        wholesale_rate_entry = tk.Entry(add_window, textvariable=wholesale_rate_var)
        wholesale_rate_entry.pack()
        
        tk.Label(add_window, text="Margin2 (%):").pack()
        margin2_entry = tk.Entry(add_window)
        margin2_entry.pack()
        
        # Retail rate entry
        retail_rate_var = tk.StringVar()
        tk.Label(add_window, text="Retail Rate:").pack()
        retail_rate_entry = tk.Entry(add_window, textvariable=retail_rate_var)
        retail_rate_entry.pack()
        
        tk.Label(add_window, text="Opening Stock:").pack()
        opening_entry = tk.Entry(add_window)
        opening_entry.pack()
        
        tk.Label(add_window, text="Purchased Stock:").pack()
        purchased_entry = tk.Entry(add_window)
        purchased_entry.pack()
        
        tk.Label(add_window, text="Sold Stock:").pack()
        sold_entry = tk.Entry(add_window)
        sold_entry.insert(0, "0")
        sold_entry.pack()
        
        tk.Label(add_window, text="Closing Stock:").pack()
        closing_label = tk.Label(add_window, text="0")
        closing_label.pack()
        
        tk.Label(add_window, text="Modified Date:").pack()
        modified_label = tk.Label(add_window, text=datetime.now().strftime("%Y-%m-%d"))
        modified_label.pack()
        
        # Function to update product suggestions
        def update_product_suggestions(event=None):
            selected_brand = brand_entry.get()
            if selected_brand:
                products = [p['Product Name'] for p in self.app.products if p['Brand'] == selected_brand]
                name_entry['values'] = products
            else:
                name_entry['values'] = []
        
        # Function to auto-fill product data
        def auto_fill_product_data(event=None):
            selected_brand = brand_entry.get()
            selected_product = name_entry.get()
            
            if selected_brand and selected_product:
                # Find existing product
                existing_product = None
                for product in self.app.products:
                    if (product['Brand'].strip().lower() == selected_brand.strip().lower() and 
                        product['Product Name'].strip().lower() == selected_product.strip().lower()):
                        existing_product = product
                        break
                
                if existing_product:
                    # Auto-fill all fields with existing data
                    purchase_entry.delete(0, tk.END)
                    purchase_entry.insert(0, existing_product.get('Purchase Rate', '0'))
                    
                    margin1_entry.delete(0, tk.END)
                    margin1_entry.insert(0, existing_product.get('Margin1 (%)', '0'))
                    
                    wholesale_rate_var.set(existing_product.get('Wholesale Rate', '0'))
                    
                    margin2_entry.delete(0, tk.END)
                    margin2_entry.insert(0, existing_product.get('Margin2 (%)', '0'))
                    
                    retail_rate_var.set(existing_product.get('Retail Rate', '0'))
                    
                    # Set opening stock to previous closing stock
                    previous_closing = existing_product.get('Closing Stock', '0')
                    opening_entry.delete(0, tk.END)
                    opening_entry.insert(0, previous_closing)
                    
                    # Reset purchased stock for new purchase entry
                    purchased_entry.delete(0, tk.END)
                    purchased_entry.insert(0, "0")
                    
                    # Set sold stock to 0 for new purchase transactions
                    sold_entry.delete(0, tk.END)
                    sold_entry.insert(0, "0")
                    
                    # Set purchase date to today for new purchase
                    date_entry.set_date(datetime.now())
        
        # Bind events
        brand_entry.bind("<<ComboboxSelected>>", lambda e: update_product_suggestions())
        brand_entry.bind("<KeyRelease>", lambda e: update_product_suggestions())
        name_entry.bind("<<ComboboxSelected>>", auto_fill_product_data)
        name_entry.bind("<KeyRelease>", auto_fill_product_data)
        
        # Calculate function
        def calculate_values(event=None):
            try:
                purchase_rate = float(purchase_entry.get() or 0)
                margin1 = float(margin1_entry.get() or 0)
                
                if margin1 == 0:
                    wholesale_rate = float(wholesale_rate_var.get() or 0)
                else:
                    wholesale_rate = round(purchase_rate * (1 + margin1 / 100), 2)
                    wholesale_rate_var.set(f"{wholesale_rate:.2f}")
                
                margin2 = float(margin2_entry.get() or 0)
                
                if margin2 == 0:
                    retail_rate = float(retail_rate_var.get() or 0)
                else:
                    retail_rate = round(wholesale_rate * (1 + margin2 / 100), 2)
                    retail_rate_var.set(f"{retail_rate:.2f}")
                
                opening = int(opening_entry.get() or 0)
                purchased = int(purchased_entry.get() or 0)
                closing = opening + purchased
                closing_label.config(text=str(closing))
                
            except ValueError:
                pass
        
        # Bind events for auto-calculation
        purchase_entry.bind("<KeyRelease>", calculate_values)
        margin1_entry.bind("<KeyRelease>", calculate_values)
        margin2_entry.bind("<KeyRelease>", calculate_values)
        opening_entry.bind("<KeyRelease>", calculate_values)
        purchased_entry.bind("<KeyRelease>", calculate_values)
        sold_entry.bind("<KeyRelease>", calculate_values)
        
        # Save function
        def save_product():
            try:
                brand = brand_entry.get()
                name = name_entry.get()
                purchase_date = date_entry.get_date().strftime("%Y-%m-%d")
                purchase_rate = float(purchase_entry.get() or 0)
                
                margin1 = float(margin1_entry.get() or 0)
                if margin1 == 0:
                    wholesale_rate = float(wholesale_rate_var.get() or 0)
                else:
                    wholesale_rate = round(purchase_rate * (1 + margin1 / 100), 2)
                
                margin2 = float(margin2_entry.get() or 0)
                if margin2 == 0:
                    retail_rate = float(retail_rate_var.get() or 0)
                else:
                    retail_rate = round(wholesale_rate * (1 + margin2 / 100), 2)
                
                new_purchased_qty = int(purchased_entry.get() or 0)
                opening = int(opening_entry.get() or 0)
                closing = opening + new_purchased_qty
                modified_date = datetime.now().strftime("%Y-%m-%d")
                
                if not brand or not name:
                    messagebox.showerror("Error", "Brand and Product Name are required")
                    return
                
                # Check if product already exists
                existing_index = -1
                for i, product in enumerate(self.app.products):
                    if product['Brand'].strip().lower() == brand.strip().lower() and \
                    product['Product Name'].strip().lower() == name.strip().lower():
                        existing_index = i
                        break
                
                if existing_index >= 0:
                    # UPDATE EXISTING PRODUCT
                    existing_product = self.app.products[existing_index]
                    
                    # Get current values
                    current_opening = int(existing_product.get('Opening Stock', 0))
                    current_purchased = int(existing_product.get('Purchased Stock', 0))
                    current_sold = int(existing_product.get('Sold Stock', 0))
                    current_closing = int(existing_product.get('Closing Stock', 0))
                    
                    # For Sales Entry->Add Product:
                    new_opening = opening  # From entry field (should be previous closing)
                    new_purchased = new_purchased_qty  # Only new purchases
                    new_sold = 0  # Keep existing sold stock
                    new_closing = new_opening + new_purchased
                    
                    # Update existing product
                    self.app.products[existing_index].update({
                        "Purchase Date": purchase_date,
                        "Purchase Rate": f"{purchase_rate:.2f}",
                        "Margin1 (%)": f"{margin1:.2f}",
                        "Wholesale Rate": f"{wholesale_rate:.2f}",
                        "Margin2 (%)": f"{margin2:.2f}",
                        "Retail Rate": f"{retail_rate:.2f}",
                        "Opening Stock": str(new_opening),
                        "Purchased Stock": str(new_purchased),
                        "Sold Stock": str(new_sold),
                        "Closing Stock": str(new_closing),
                        "Modified Date": modified_date
                    })
                    
                    action_message = f"Product updated successfully!\nOpening Stock: {new_opening}\nNew Purchased: {new_purchased}\nClosing Stock: {new_closing}"
                else:
                    # Add new product
                    new_product = {
                        "Brand": brand,
                        "Product Name": name,
                        "Purchase Date": purchase_date,
                        "Purchase Rate": f"{purchase_rate:.2f}",
                        "Margin1 (%)": f"{margin1:.2f}",
                        "Wholesale Rate": f"{wholesale_rate:.2f}",
                        "Margin2 (%)": f"{margin2:.2f}",
                        "Retail Rate": f"{retail_rate:.2f}",
                        "Opening Stock": str(opening),
                        "Purchased Stock": str(new_purchased_qty),
                        "Sold Stock": "0",
                        "Closing Stock": str(closing),
                        "Modified Date": modified_date
                    }
                    self.app.products.append(new_product)
                    action_message = "New product added successfully!"
                
                # Save to CSV - IMPORT HERE TO AVOID CIRCULAR IMPORT
                try:
                    from models.product import ProductModel
                except ImportError:
                    # Try relative import
                    from ..models.product import ProductModel
                
                if ProductModel.save_products(self.app.products):
                    # Reload products
                    self.app.load_products()
                    messagebox.showinfo("Success", action_message)
                    add_window.destroy()
            
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        # Save button
        tk.Button(add_window, text="Save Product", command=save_product).pack(pady=20)
        
        # Initialize product suggestions
        update_product_suggestions()

    def get_brands(self):
        """Get unique brands from products"""
        return sorted(set(p["Brand"] for p in self.app.products))
    
    def view_products(self):
        """Open view products window - FULL implementation"""
        print("📋 Opening View Products...")
        
        view_window = tk.Toplevel(self.app.root)
        view_window.title("Product List")
        view_window.geometry("1200x600")
        
        # Treeview with scrollbars
        tree_frame = tk.Frame(view_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_y = tk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        tree = ttk.Treeview(tree_frame, columns=(
            "Brand", "Product", "Purchase Date", "Purchase Rate", "Margin1", 
            "Wholesale", "Margin2", "Retail", "Opening", "Purchased", 
            "Sold", "Closing", "Modified"
        ), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        # Configure columns to align left
        tree.heading("Brand", text="Brand", anchor="w")
        tree.heading("Product", text="Product", anchor="w")
        tree.heading("Purchase Date", text="Purchase Date", anchor="w")
        tree.heading("Purchase Rate", text="Purchase Rate", anchor="e")
        tree.heading("Margin1", text="Margin1 (%)", anchor="e")
        tree.heading("Wholesale", text="Wholesale", anchor="e")
        tree.heading("Margin2", text="Margin2 (%)", anchor="e")
        tree.heading("Retail", text="Retail", anchor="e")
        tree.heading("Opening", text="Opening", anchor="e")
        tree.heading("Purchased", text="Purchased", anchor="e")
        tree.heading("Sold", text="Sold", anchor="e")
        tree.heading("Closing", text="Closing", anchor="e")
        tree.heading("Modified", text="Modified", anchor="w")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Brand", width=100, anchor="w")
        tree.column("Product", width=150, anchor="w")
        tree.column("Purchase Date", width=100, anchor="w")
        tree.column("Purchase Rate", width=80, anchor="e")
        tree.column("Margin1", width=70, anchor="e")
        tree.column("Wholesale", width=80, anchor="e")
        tree.column("Margin2", width=70, anchor="e")
        tree.column("Retail", width=80, anchor="e")
        tree.column("Opening", width=70, anchor="e")
        tree.column("Purchased", width=70, anchor="e")
        tree.column("Sold", width=70, anchor="e")
        tree.column("Closing", width=70, anchor="e")
        tree.column("Modified", width=100, anchor="w")
        
        # Add data to treeview
        for product in self.app.products:
            tree.insert("", tk.END, values=(
                product.get("Brand", ""),
                product.get("Product Name", ""),
                product.get("Purchase Date", ""),
                product.get("Purchase Rate", "0"),
                product.get("Margin1 (%)", "0"),
                product.get("Wholesale Rate", "0"),
                product.get("Margin2 (%)", "0"),
                product.get("Retail Rate", "0"),
                product.get("Opening Stock", "0"),
                product.get("Purchased Stock", "0"),
                product.get("Sold Stock", "0"),
                product.get("Closing Stock", "0"),
                product.get("Modified Date", "")
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Add delete button for admin
        btn_frame = tk.Frame(view_window)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Use lambda with proper self reference
        tk.Button(btn_frame, text="Delete Selected", 
                command=lambda t=tree: self.delete_product(t)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Refresh", 
                command=lambda t=tree, w=view_window: self.refresh_products_view(t, w)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Export to CSV", 
                command=self.export_products_to_csv).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", 
                command=view_window.destroy).pack(side=tk.RIGHT, padx=5)

    def delete_product(self, tree):
        """Delete selected product"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to delete")
            return
            
        item = tree.item(selected[0])
        values = item['values']
        
        if not messagebox.askyesno("Confirm", f"Delete product {values[1]}?"):
            return
            
        # Remove from products list
        self.app.products = [p for p in self.app.products 
                            if not (p.get("Brand", "") == values[0] and 
                                p.get("Product Name", "") == values[1])]
        
        # Try to save to CSV - IMPORT HERE
        try:
            try:
                from models.product import ProductModel
            except ImportError:
                from ..models.product import ProductModel
            
            if ProductModel.save_products(self.app.products):
                messagebox.showinfo("Success", "Product deleted successfully!")
                # Refresh the view
                self.refresh_products_view(tree, tree.master.master)  # Get toplevel window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def refresh_products_view(self, tree, window):
        """Refresh the products view"""
        # Reload products
        self.app.load_products()
        
        # Clear the tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Add data to treeview
        for product in self.app.products:
            tree.insert("", tk.END, values=(
                product.get("Brand", ""),
                product.get("Product Name", ""),
                product.get("Purchase Date", ""),
                product.get("Purchase Rate", "0"),
                product.get("Margin1 (%)", "0"),
                product.get("Wholesale Rate", "0"),
                product.get("Margin2 (%)", "0"),
                product.get("Retail Rate", "0"),
                product.get("Opening Stock", "0"),
                product.get("Purchased Stock", "0"),
                product.get("Sold Stock", "0"),
                product.get("Closing Stock", "0"),
                product.get("Modified Date", "")
            ))

    def export_products_to_csv(self):
        """Export products to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save products as"
        )
        
        if not filename:
            return
            
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                writer.writerow([
                    "Brand", "Product Name", "Purchase Date", "Purchase Rate", 
                    "Margin1 (%)", "Wholesale Rate", "Margin2 (%)", "Retail Rate",
                    "Opening Stock", "Purchased Stock", "Sold Stock", "Closing Stock", "Modified Date"
                ])
                
                # Write data
                for product in self.app.products:
                    writer.writerow([
                        product.get("Brand", ""),
                        product.get("Product Name", ""),
                        product.get("Purchase Date", ""),
                        product.get("Purchase Rate", "0"),
                        product.get("Margin1 (%)", "0"),
                        product.get("Wholesale Rate", "0"),
                        product.get("Margin2 (%)", "0"),
                        product.get("Retail Rate", "0"),
                        product.get("Opening Stock", "0"),
                        product.get("Purchased Stock", "0"),
                        product.get("Sold Stock", "0"),
                        product.get("Closing Stock", "0"),
                        product.get("Modified Date", "")
                    ])
            
            messagebox.showinfo("Success", f"Products exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export products: {str(e)}")
    
    def rate_change_window(self):
        """Open rate change window"""
        print("💰 Opening Rate Change Window...")
        messagebox.showinfo("Rate Change", "Rate Change feature will be implemented soon")
    
    def sales_receipt_window(self):
        """Open sales receipt window"""
        print("🧾 Opening Sales Receipt Window...")
        messagebox.showinfo("Sales Receipt", "Sales Receipt feature will be implemented soon")
    
    # Helper method to load customers without import issues
    def _load_customers(self):
        """Load customers from CSV file"""
        if not os.path.exists("customers.csv"):
            return []
            
        customers = []
        try:
            with open("customers.csv", mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customers.append({
                        "Name": row.get("Name", ""),
                        "Phone": row.get("Phone", ""),
                        "Place": row.get("Place", ""),
                        "Site": row.get("Site", "")
                    })
        except Exception as e:
            print(f"Error loading customers: {str(e)}")
        return customers
    
    def view_customers(self):
        """Open view customers window - FULL implementation"""
        print("👥 Opening View Customers...")
        
        customers = self._load_customers()
        
        view_window = tk.Toplevel(self.app.root)
        view_window.title("Customer List")
        view_window.geometry("800x400")
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(view_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_y = tk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("Name", "Phone", "Place", "Site"), yscrollcommand=scroll_y.set)
        scroll_y.config(command=tree.yview)
        
        tree.heading("Name", text="Name", anchor="w")
        tree.heading("Phone", text="Phone", anchor="w")
        tree.heading("Place", text="Place", anchor="w")
        tree.heading("Site", text="Site", anchor="w")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Name", width=200, anchor="w")
        tree.column("Phone", width=150, anchor="w")
        tree.column("Place", width=150, anchor="w")
        tree.column("Site", width=150, anchor="w")
        
        for customer in customers:
            tree.insert("", tk.END, values=(
                customer.get('Name', ''),
                customer.get('Phone', ''),
                customer.get('Place', ''),
                customer.get('Site', '')
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(view_window)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Refresh", 
                command=lambda t=tree: self.refresh_customers_view(t)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Export to CSV", 
                command=self.export_customers_to_csv).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", 
                command=view_window.destroy).pack(side=tk.RIGHT, padx=5)

    def refresh_customers_view(self, tree):
        """Refresh the customers view"""
        customers = self._load_customers()
        
        # Clear the tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Add data
        for customer in customers:
            tree.insert("", tk.END, values=(
                customer.get('Name', ''),
                customer.get('Phone', ''),
                customer.get('Place', ''),
                customer.get('Site', '')
            ))

    def export_customers_to_csv(self):
        """Export customers to CSV file"""
        customers = self._load_customers()
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save customers as"
        )
        
        if not filename:
            return
            
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                writer.writerow(["Name", "Phone", "Place", "Site"])
                
                # Write data
                for customer in customers:
                    writer.writerow([
                        customer.get('Name', ''),
                        customer.get('Phone', ''),
                        customer.get('Place', ''),
                        customer.get('Site', '')
                    ])
            
            messagebox.showinfo("Success", f"Customers exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export customers: {str(e)}")
    
    def purchase_entry_window(self):
        """Open purchase entry window"""
        print("🛒 Opening Purchase Entry Window...")
        messagebox.showinfo("Purchase Entry", "Purchase Entry feature will be implemented soon")
    
    def view_purchases(self):
        """Open view purchases window"""
        print("📊 Opening View Purchases...")
        messagebox.showinfo("View Purchases", "View Purchases feature will be implemented soon")
    
    def purchase_receipt_window(self):
        """Open purchase receipt window"""
        print("🧾 Opening Purchase Receipt Window...")
        messagebox.showinfo("Purchase Receipt", "Purchase Receipt feature will be implemented soon")
    
    def view_stocks(self):
        """Open stock summary window - FULL implementation"""
        print("📦 Opening Stock Summary...")
        
        view_window = tk.Toplevel(self.app.root)
        view_window.title("Stock Summary")
        view_window.geometry("800x600")
        
        # Refresh products data first
        self.app.load_products()
        
        # Treeview with scrollbars
        tree_frame = tk.Frame(view_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_y = tk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        tree = ttk.Treeview(tree_frame, columns=(
            "Brand", "Product", "Opening", "Purchased", "Sold", "Closing"
        ), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        tree.heading("Brand", text="Brand", anchor="w")
        tree.heading("Product", text="Product", anchor="w")
        tree.heading("Opening", text="Opening Stock", anchor="e")
        tree.heading("Purchased", text="Purchased Stock", anchor="e")
        tree.heading("Sold", text="Sold Stock", anchor="e")
        tree.heading("Closing", text="Closing Stock", anchor="e")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Brand", width=150, anchor="w")
        tree.column("Product", width=200, anchor="w")
        tree.column("Opening", width=100, anchor="e")
        tree.column("Purchased", width=100, anchor="e")
        tree.column("Sold", width=100, anchor="e")
        tree.column("Closing", width=100, anchor="e")
        
        # Add debug information
        print(f"DEBUG: Displaying {len(self.app.products)} products in Stock Summary")
        
        for product in self.app.products:
            brand = product.get("Brand", "")
            product_name = product.get("Product Name", "")
            opening = product.get("Opening Stock", "0")
            purchased = product.get("Purchased Stock", "0")
            sold = product.get("Sold Stock", "0")
            closing = product.get("Closing Stock", "0")
            
            tree.insert("", tk.END, values=(
                brand,
                product_name,
                opening,
                purchased,
                sold,
                closing
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Add summary statistics
        total_opening = sum(int(p.get("Opening Stock", 0)) for p in self.app.products)
        total_purchased = sum(int(p.get("Purchased Stock", 0)) for p in self.app.products)
        total_sold = sum(int(p.get("Sold Stock", 0)) for p in self.app.products)
        total_closing = sum(int(p.get("Closing Stock", 0)) for p in self.app.products)
        
        summary_frame = tk.Frame(view_window)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(summary_frame, text=f"Total Products: {len(self.app.products)}", 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Total Opening: {total_opening}", 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Total Purchased: {total_purchased}", 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Total Sold: {total_sold}", 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Total Closing: {total_closing}", 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(view_window)
        btn_frame.pack(fill=tk.X, pady=5)
        
        def refresh_stock_view():
            # Clear the tree
            for item in tree.get_children():
                tree.delete(item)
            
            # Reload products and refresh the view
            self.app.load_products()
            
            # Repopulate the tree
            for product in self.app.products:
                tree.insert("", tk.END, values=(
                    product.get("Brand", ""),
                    product.get("Product Name", ""),
                    product.get("Opening Stock", "0"),
                    product.get("Purchased Stock", "0"),
                    product.get("Sold Stock", "0"),
                    product.get("Closing Stock", "0")
                ))
            
            # Update summary
            total_opening = sum(int(p.get("Opening Stock", 0)) for p in self.app.products)
            total_purchased = sum(int(p.get("Purchased Stock", 0)) for p in self.app.products)
            total_sold = sum(int(p.get("Sold Stock", 0)) for p in self.app.products)
            total_closing = sum(int(p.get("Closing Stock", 0)) for p in self.app.products)
            
            for widget in summary_frame.winfo_children():
                widget.destroy()
            
            tk.Label(summary_frame, text=f"Total Products: {len(self.app.products)}", 
                    font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
            tk.Label(summary_frame, text=f"Total Opening: {total_opening}", 
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
            tk.Label(summary_frame, text=f"Total Purchased: {total_purchased}", 
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
            tk.Label(summary_frame, text=f"Total Sold: {total_sold}", 
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
            tk.Label(summary_frame, text=f"Total Closing: {total_closing}", 
                    font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Refresh", command=refresh_stock_view).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export to CSV", 
                command=self.export_stock_to_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=view_window.destroy).pack(side=tk.RIGHT, padx=5)

    def export_stock_to_csv(self):
        """Export stock summary to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save stock summary as"
        )
        
        if not filename:
            return
            
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                writer.writerow(["Brand", "Product Name", "Opening Stock", "Purchased Stock", 
                            "Sold Stock", "Closing Stock"])
                
                # Write data
                for product in self.app.products:
                    writer.writerow([
                        product.get("Brand", ""),
                        product.get("Product Name", ""),
                        product.get("Opening Stock", "0"),
                        product.get("Purchased Stock", "0"),
                        product.get("Sold Stock", "0"),
                        product.get("Closing Stock", "0")
                    ])
            
            messagebox.showinfo("Success", f"Stock summary exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export stock summary: {str(e)}")
    
    def view_purchase_receipts(self):
        """Open purchase receipt summary"""
        print("📋 Opening Purchase Receipt Summary...")
        messagebox.showinfo("Purchase Receipt Summary", "Purchase Receipt Summary feature will be implemented soon")
    
    def view_sales_receipts(self):
        """Open sales receipt summary"""
        print("📋 Opening Sales Receipt Summary...")
        messagebox.showinfo("Sales Receipt Summary", "Sales Receipt Summary feature will be implemented soon")
    
    def generate_sales_report(self, report_type):
        """Generate sales report"""
        print(f"📈 Generating {report_type} report...")
        try:
            from ..utils.reports import ReportGenerator
            ReportGenerator.generate_sales_report(self.app, report_type)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    # UPDATE THESE METHODS in src/admin_features.py:

    def rate_change_window(self):
        """Open rate change window - FIXED"""
        print("💰 Opening Rate Change Window...")
        try:
            from .ui.dialogs import Dialogs
            Dialogs.create_rate_change_window(self.app)
        except ImportError:
            try:
                from src.app.ui.dialogs import Dialogs
                Dialogs.create_rate_change_window(self.app)
            except Exception as e:
                print(f"Error opening rate change window: {e}")
                messagebox.showerror("Error", f"Failed to open rate change window: {str(e)}")
    
    def sales_receipt_window(self):
        """Open sales receipt window - FIXED"""
        print("🧾 Opening Sales Receipt Window...")
        try:
            from .ui.dialogs import Dialogs
            Dialogs.create_sales_receipt_window(self.app)
        except ImportError:
            try:
                from src.app.ui.dialogs import Dialogs
                Dialogs.create_sales_receipt_window(self.app)
            except Exception as e:
                print(f"Error opening sales receipt window: {e}")
                messagebox.showerror("Error", f"Failed to open sales receipt window: {str(e)}")
    
    def purchase_entry_window(self):
        """Open purchase entry window - FIXED"""
        print("🛒 Opening Purchase Entry Window...")
        try:
            from .ui.dialogs import Dialogs
            Dialogs.create_purchase_entry_window(self.app)
        except ImportError:
            try:
                from src.app.ui.dialogs import Dialogs
                Dialogs.create_purchase_entry_window(self.app)
            except Exception as e:
                print(f"Error opening purchase entry window: {e}")
                messagebox.showerror("Error", f"Failed to open purchase entry window: {str(e)}")

    def generate_sales_report(self, report_type):
        """Generate sales report"""
        print(f"📈 Generating {report_type} report...")
        try:
            # Try relative import first
            try:
                from ..utils.reports import ReportGenerator
            except ImportError:
                # Try absolute import
                from src.utils.reports import ReportGenerator
            
            ReportGenerator.generate_sales_report(self.app, report_type)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")