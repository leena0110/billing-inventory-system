# src/app/ui/dialogs.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import csv
import os

# Correct imports - using relative imports
from ..config.colors import COLORS, FONTS

class Dialogs:
    """Dialog windows for various features"""
    
    @staticmethod
    def get_brands(app):
        """Get unique brands from products"""
        return sorted(set(p.get("Brand", "") for p in app.products))
    
    @staticmethod
    def create_rate_change_window(app):
        """Create rate change dialog window"""
        rate_window = tk.Toplevel(app.root)
        rate_window.title("Rate Change Management")
        rate_window.geometry("800x600")
        
        # Brand selection
        brand_frame = tk.Frame(rate_window)
        brand_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(brand_frame, text="Select Brand:").pack(side=tk.LEFT)
        brand_combo = ttk.Combobox(brand_frame, values=Dialogs.get_brands(app), width=30)
        brand_combo.pack(side=tk.LEFT, padx=5)
        
        # Product selection
        product_frame = tk.Frame(rate_window)
        product_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(product_frame, text="Select Product:").pack(side=tk.LEFT)
        product_combo = ttk.Combobox(product_frame, width=40)
        product_combo.pack(side=tk.LEFT, padx=5)
        
        def update_products(*args):
            selected_brand = brand_combo.get()
            products = [p.get('Product Name', '') for p in app.products if p.get('Brand', '') == selected_brand]
            product_combo['values'] = products
            if products:
                product_combo.set(products[0])
        
        brand_combo.bind("<<ComboboxSelected>>", update_products)
        
        # Date selection
        date_frame = tk.Frame(rate_window)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(date_frame, text="Effective Date:").pack(side=tk.LEFT)
        date_entry = DateEntry(date_frame, width=12, background='darkblue', 
                            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.pack(side=tk.LEFT, padx=5)
        
        # Current rate info
        current_frame = tk.Frame(rate_window)
        current_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(current_frame, text="Current Purchase Rate:").grid(row=0, column=0, sticky="w")
        current_rate_label = tk.Label(current_frame, text="0.00", font=("Arial", 10, "bold"))
        current_rate_label.grid(row=0, column=1, padx=5, sticky="w")
        
        tk.Label(current_frame, text="Current Effective Date:").grid(row=1, column=0, sticky="w")
        current_date_label = tk.Label(current_frame, text="", font=("Arial", 10))
        current_date_label.grid(row=1, column=1, padx=5, sticky="w")
        
        # Rate entry frame
        entry_frame = tk.Frame(rate_window)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(entry_frame, text="New Purchase Rate:").grid(row=0, column=0, sticky="w")
        purchase_entry = tk.Entry(entry_frame)
        purchase_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(entry_frame, text="Margin1 (%):").grid(row=1, column=0, sticky="w")
        margin1_entry = tk.Entry(entry_frame)
        margin1_entry.grid(row=1, column=1, padx=5)
        
        # Wholesale rate entry
        wholesale_rate_var = tk.StringVar()
        tk.Label(entry_frame, text="Wholesale Rate:").grid(row=2, column=0, sticky="w")
        wholesale_rate_entry = tk.Entry(entry_frame, textvariable=wholesale_rate_var)
        wholesale_rate_entry.grid(row=2, column=1, padx=5, sticky="w")
        
        tk.Label(entry_frame, text="Margin2 (%):").grid(row=3, column=0, sticky="w")
        margin2_entry = tk.Entry(entry_frame)
        margin2_entry.grid(row=3, column=1, padx=5)
        
        # Retail rate entry
        retail_rate_var = tk.StringVar()
        tk.Label(entry_frame, text="Retail Rate:").grid(row=4, column=0, sticky="w")
        retail_rate_entry = tk.Entry(entry_frame, textvariable=retail_rate_var)
        retail_rate_entry.grid(row=4, column=1, padx=5, sticky="w")
        
        # Modified date
        tk.Label(entry_frame, text="Modified Date:").grid(row=5, column=0, sticky="w")
        modified_label = tk.Label(entry_frame, text=datetime.now().strftime("%Y-%m-%d"))
        modified_label.grid(row=5, column=1, padx=5, sticky="w")
        
        # Calculate button
        def calculate_rates():
            try:
                purchase_rate = float(purchase_entry.get())
                margin1 = float(margin1_entry.get() or 0)
                
                if margin1 == 0:
                    wholesale_rate = float(wholesale_rate_var.get())
                else:
                    wholesale_rate = round(purchase_rate * (1 + margin1 / 100), 2)
                    wholesale_rate_var.set(f"{wholesale_rate:.2f}")
                
                margin2 = float(margin2_entry.get() or 0)
                
                if margin2 == 0:
                    retail_rate = float(retail_rate_var.get())
                else:
                    retail_rate = round(wholesale_rate * (1 + margin2 / 100), 2)
                    retail_rate_var.set(f"{retail_rate:.2f}")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for rates and margins")
        
        calc_button = tk.Button(rate_window, text="Calculate Rates", command=calculate_rates)
        calc_button.pack(pady=5)
        
        # Load button
        def load_product_data():
            selected_product = product_combo.get()
            if not selected_product:
                return
                
            product = next((p for p in app.products if p.get('Product Name', '') == selected_product), None)
            if product:
                current_rate_label.config(text=product.get('Purchase Rate', '0'))
                current_date_label.config(text=product.get('Purchase Date', 'Not set'))
                
                purchase_entry.delete(0, tk.END)
                purchase_entry.insert(0, product.get('Purchase Rate', '0'))
                
                margin1_entry.delete(0, tk.END)
                margin1_entry.insert(0, product.get('Margin1 (%)', '0'))
                
                margin2_entry.delete(0, tk.END)
                margin2_entry.insert(0, product.get('Margin2 (%)', '0'))
                
                wholesale_rate_var.set(product.get('Wholesale Rate', '0'))
                retail_rate_var.set(product.get('Retail Rate', '0'))
                
                tomorrow = datetime.now() + timedelta(days=1)
                date_entry.set_date(tomorrow)
        
        load_button = tk.Button(rate_window, text="Load Product Data", command=load_product_data)
        load_button.pack(pady=5)
        
        # Save button
        def save_rate_changes():
            selected_product = product_combo.get()
            if not selected_product:
                messagebox.showerror("Error", "Please select a product")
                return
                
            try:
                new_purchase_rate = float(purchase_entry.get())
                effective_date = date_entry.get_date().strftime("%Y-%m-%d")
                modified_date = datetime.now().strftime("%Y-%m-%d")
                
                margin1 = float(margin1_entry.get() or 0)
                if margin1 == 0:
                    wholesale_rate = float(wholesale_rate_var.get())
                else:
                    wholesale_rate = round(new_purchase_rate * (1 + margin1 / 100), 2)
                
                margin2 = float(margin2_entry.get() or 0)
                if margin2 == 0:
                    retail_rate = float(retail_rate_var.get())
                else:
                    retail_rate = round(wholesale_rate * (1 + margin2 / 100), 2)
                
                # Check if this is a future date rate change
                effective_datetime = datetime.strptime(effective_date, "%Y-%m-%d")
                current_datetime = datetime.now()
                
                if effective_datetime.date() > current_datetime.date():
                    # Future rate change
                    Dialogs.save_future_rate_change(
                        selected_product, 
                        new_purchase_rate, 
                        effective_date,
                        margin1, 
                        wholesale_rate, 
                        margin2, 
                        retail_rate, 
                        modified_date
                    )
                    messagebox.showinfo("Success", 
                        f"Future rate change scheduled!\n"
                        f"New rate: ₹{new_purchase_rate:.2f} will be effective from {effective_date}")
                else:
                    # Immediate rate change
                    Dialogs.update_product_rate_immediate(app,
                        selected_product,
                        new_purchase_rate,
                        effective_date,
                        margin1,
                        wholesale_rate,
                        margin2,
                        retail_rate,
                        modified_date
                    )
                    messagebox.showinfo("Success", "Product rates updated successfully!")
                
                rate_window.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for rates and margins")
        
        save_button = tk.Button(rate_window, text="Save Rate Changes", command=save_rate_changes)
        save_button.pack(pady=10)
        
        # Initialize
        if Dialogs.get_brands(app):
            brand_combo.set(Dialogs.get_brands(app)[0])
            update_products()
    
    @staticmethod
    def save_future_rate_change(product_name, new_purchase_rate, effective_date,
                               margin1, wholesale_rate, margin2, retail_rate, modified_date):
        """Save future rate changes to a separate file"""
        future_changes = []
        
        # Load existing future changes
        if os.path.exists("future_rate_changes.csv"):
            try:
                with open("future_rate_changes.csv", mode="r", encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    future_changes = list(reader)
            except Exception as e:
                print(f"Error loading future rate changes: {e}")
        
        # Remove any existing future changes for this product
        future_changes = [fc for fc in future_changes if fc.get('Product Name', '') != product_name]
        
        # Add the new future change
        future_changes.append({
            'Product Name': product_name,
            'New Purchase Rate': f"{new_purchase_rate:.2f}",
            'Effective Date': effective_date,
            'Margin1 (%)': f"{margin1:.2f}",
            'Wholesale Rate': f"{wholesale_rate:.2f}",
            'Margin2 (%)': f"{margin2:.2f}",
            'Retail Rate': f"{retail_rate:.2f}",
            'Modified Date': modified_date
        })
        
        # Save future changes
        try:
            with open("future_rate_changes.csv", mode="w", newline="", encoding='utf-8') as file:
                fieldnames = ['Product Name', 'New Purchase Rate', 'Effective Date', 
                            'Margin1 (%)', 'Wholesale Rate', 'Margin2 (%)', 
                            'Retail Rate', 'Modified Date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(future_changes)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save future rate change: {str(e)}")
    
    @staticmethod
    def update_product_rate_immediate(app, product_name, new_purchase_rate, effective_date,
                                    margin1, wholesale_rate, margin2, retail_rate, modified_date):
        """Update product rate immediately"""
        from ..models.product import ProductModel
        
        for p in app.products:
            if p.get('Product Name', '') == product_name:
                p.update({
                    'Purchase Rate': f"{new_purchase_rate:.2f}",
                    'Purchase Date': effective_date,
                    'Margin1 (%)': f"{margin1:.2f}",
                    'Wholesale Rate': f"{wholesale_rate:.2f}",
                    'Margin2 (%)': f"{margin2:.2f}",
                    'Retail Rate': f"{retail_rate:.2f}",
                    'Modified Date': modified_date
                })
                break
        
        # Save to CSV
        try:
            ProductModel.save_products(app.products)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save products: {str(e)}")
    
    @staticmethod
    def create_purchase_entry_window(app):
        """Create purchase entry window"""
        from ..utils.file_operations import load_customers, get_purchase_bill_number
        
        purchase_window = tk.Toplevel(app.root)
        purchase_window.title("Purchase Entry")
        purchase_window.geometry("1000x600")
        
        # Frame for purchase details
        details_frame = tk.Frame(purchase_window)
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Supplier name with autocomplete
        tk.Label(details_frame, text="Supplier Name:").grid(row=0, column=0, sticky="w")
        supplier_name_combo = ttk.Combobox(details_frame, width=30)
        supplier_name_combo.grid(row=0, column=1, sticky="w", padx=5)
        
        # Load supplier suggestions
        customers = load_customers()
        supplier_name_combo['values'] = [c.get('Name', '') for c in customers if c.get('Name')]
        
        # Supplier phone
        tk.Label(details_frame, text="Phone No:").grid(row=1, column=0, sticky="w")
        supplier_phone_entry = tk.Entry(details_frame, width=30)
        supplier_phone_entry.grid(row=1, column=1, sticky="w", padx=5)
        
        # Bill number
        tk.Label(details_frame, text="Bill No:").grid(row=0, column=2, sticky="w", padx=10)
        purchase_bill_entry = tk.Entry(details_frame, width=15)
        purchase_bill_entry.grid(row=0, column=3, sticky="w")
        purchase_bill_entry.insert(0, get_purchase_bill_number())
        
        # Date
        tk.Label(details_frame, text="Date:").grid(row=0, column=4, sticky="w", padx=10)
        purchase_date_entry = DateEntry(details_frame, width=12, background='darkblue', 
                                       foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        purchase_date_entry.grid(row=0, column=5, sticky="w")
        
        # Place and Site
        tk.Label(details_frame, text="Place:").grid(row=0, column=6, sticky="w", padx=10)
        purchase_place_combo = ttk.Combobox(details_frame, width=20)
        purchase_place_combo.grid(row=0, column=7, sticky="w")
        
        tk.Label(details_frame, text="Site:").grid(row=1, column=6, sticky="w", padx=10)
        purchase_site_combo = ttk.Combobox(details_frame, width=20)
        purchase_site_combo.grid(row=1, column=7, sticky="w")
        
        # Product selection frame
        product_frame = tk.Frame(purchase_window)
        product_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Brand selection
        tk.Label(product_frame, text="Select Brand:").grid(row=0, column=0, sticky="w")
        purchase_brand_combo = ttk.Combobox(product_frame, values=Dialogs.get_brands(app), width=25)
        purchase_brand_combo.grid(row=0, column=1, sticky="w", padx=5)
        
        # Product selection
        tk.Label(product_frame, text="Select Product:").grid(row=1, column=0, sticky="w", pady=5)
        purchase_product_combo = ttk.Combobox(product_frame, width=25)
        purchase_product_combo.grid(row=1, column=1, sticky="w", padx=5)
        
        # Quantity entry
        tk.Label(product_frame, text="Qty:").grid(row=1, column=2, sticky="w", padx=5)
        purchase_qty_entry = tk.Entry(product_frame, width=5)
        purchase_qty_entry.grid(row=1, column=3, sticky="w")
        purchase_qty_entry.insert(0, "1")
        
        # Purchase Rate entry
        tk.Label(product_frame, text="Purchase Rate:").grid(row=1, column=4, sticky="w", padx=5)
        purchase_rate_entry = tk.Entry(product_frame, width=10)
        purchase_rate_entry.grid(row=1, column=5, sticky="w")
        
        # Add item button
        def add_purchase_item():
            brand = purchase_brand_combo.get()
            product = purchase_product_combo.get()
            
            try:
                qty = float(purchase_qty_entry.get())
                rate = float(purchase_rate_entry.get())
                if qty <= 0:
                    messagebox.showerror("Error", "Quantity must be positive")
                    return
                if rate < 0:
                    messagebox.showerror("Error", "Purchase rate must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity or rate")
                return
            
            total = qty * rate
            
            # Add to purchase tree
            item_count = len(purchase_tree.get_children())
            purchase_tree.insert("", tk.END, values=(
                item_count + 1,
                brand,
                product,
                f"{qty:.2f}",
                f"{rate:.2f}",
                f"{total:.2f}",
                "❌"
            ))
            
            # Reset quantity and rate
            purchase_qty_entry.delete(0, tk.END)
            purchase_qty_entry.insert(0, "1")
            purchase_rate_entry.delete(0, tk.END)
            
            # Update total
            update_purchase_total()
        
        tk.Button(product_frame, text="Add Item", command=add_purchase_item).grid(row=1, column=6, padx=5)
        
        # Purchase items treeview
        tree_frame = tk.Frame(purchase_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scroll_y = tk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        purchase_tree = ttk.Treeview(tree_frame, columns=("sno", "brand", "product", "qty", "rate", "total", "delete"), 
                                    show="headings", height=5, yscrollcommand=scroll_y.set)
        scroll_y.config(command=purchase_tree.yview)
        
        purchase_tree.heading("sno", text="S.No")
        purchase_tree.heading("brand", text="Brand")
        purchase_tree.heading("product", text="Product")
        purchase_tree.heading("qty", text="Qty")
        purchase_tree.heading("rate", text="Purchase Rate")
        purchase_tree.heading("total", text="Total")
        purchase_tree.heading("delete", text="")
        
        purchase_tree.column("sno", width=50, anchor="center")
        purchase_tree.column("brand", width=100, anchor="w")
        purchase_tree.column("product", width=150, anchor="w")
        purchase_tree.column("qty", width=80, anchor="e")
        purchase_tree.column("rate", width=100, anchor="e")
        purchase_tree.column("total", width=100, anchor="e")
        purchase_tree.column("delete", width=50, anchor="center")
        
        purchase_tree.pack(fill=tk.BOTH, expand=True)
        
        def delete_purchase_item(event):
            item = purchase_tree.identify_row(event.y)
            col = purchase_tree.identify_column(event.x)
            
            if col == "#7":  # Delete column
                purchase_tree.delete(item)
                # Renumber remaining items
                for i, child in enumerate(purchase_tree.get_children(), 1):
                    values = list(purchase_tree.item(child)['values'])
                    values[0] = i
                    purchase_tree.item(child, values=values)
                update_purchase_total()
        
        purchase_tree.bind("<Double-1>", delete_purchase_item)
        
        # Payment type selection
        payment_frame = tk.Frame(purchase_window)
        payment_frame.pack(fill=tk.X, padx=10, pady=5)
        
        purchase_payment_type = tk.StringVar(value="Cash")
        tk.Label(payment_frame, text="Payment Type:").pack(side=tk.LEFT)
        tk.Radiobutton(payment_frame, text="Cash", variable=purchase_payment_type, value="Cash").pack(side=tk.LEFT)
        tk.Radiobutton(payment_frame, text="Credit", variable=purchase_payment_type, value="Credit").pack(side=tk.LEFT)
        
        # Amount paid and remaining amount
        amount_frame = tk.Frame(purchase_window)
        amount_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(amount_frame, text="Amount Paid:").pack(side=tk.LEFT)
        purchase_amount_paid_entry = tk.Entry(amount_frame, width=15)
        purchase_amount_paid_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(amount_frame, text="Remaining Amount:").pack(side=tk.LEFT, padx=5)
        purchase_remaining_amount_label = tk.Label(amount_frame, text="0.00")
        purchase_remaining_amount_label.pack(side=tk.LEFT)
        
        def update_purchase_remaining_amount(event=None):
            try:
                total = 0.0
                for child in purchase_tree.get_children():
                    values = purchase_tree.item(child)['values']
                    total += float(values[5])  # Total column
                
                amount_paid = float(purchase_amount_paid_entry.get() or 0)
                remaining = max(0, total - amount_paid)
                purchase_remaining_amount_label.config(text=f"{remaining:.2f}")
            except ValueError:
                purchase_remaining_amount_label.config(text="0.00")
        
        purchase_amount_paid_entry.bind("<KeyRelease>", update_purchase_remaining_amount)
        
        # Total amount label
        purchase_total_label = tk.Label(payment_frame, text="Total: 0.00", font=("Arial", 10, "bold"))
        purchase_total_label.pack(side=tk.RIGHT, padx=10)
        
        def update_purchase_total():
            total = 0.0
            for child in purchase_tree.get_children():
                values = purchase_tree.item(child)['values']
                total += float(values[5])  # Total column
            purchase_total_label.config(text=f"Total: {total:.2f}")
        
        def update_purchase_product_list():
            selected_brand = purchase_brand_combo.get()
            products = [p.get('Product Name', '') for p in app.products if p.get('Brand', '') == selected_brand]
            purchase_product_combo['values'] = products
            if products:
                purchase_product_combo.set(products[0])
        
        purchase_brand_combo.bind("<<ComboboxSelected>>", lambda e: update_purchase_product_list())
        
        # Auto-fill supplier details
        def auto_fill_supplier(event):
            selected_name = supplier_name_combo.get()
            for customer in customers:
                if customer.get('Name', '') == selected_name:
                    supplier_phone_entry.delete(0, tk.END)
                    supplier_phone_entry.insert(0, customer.get('Phone', ''))
                    purchase_place_combo.set(customer.get('Place', ''))
                    purchase_site_combo.set(customer.get('Site', ''))
                    break
        
        supplier_name_combo.bind("<<ComboboxSelected>>", auto_fill_supplier)
        
        # Save button
        def save_purchase():
            from ..utils.calculations import update_closing_stock
            from ..models.product import ProductModel
            
            supplier_name = supplier_name_combo.get()
            supplier_phone = supplier_phone_entry.get()
            bill_no = purchase_bill_entry.get()
            date = purchase_date_entry.get_date().strftime("%Y-%m-%d")
            place = purchase_place_combo.get()
            site = purchase_site_combo.get()
            payment_type = purchase_payment_type.get()
            
            try:
                amount_paid = float(purchase_amount_paid_entry.get() or 0)
            except ValueError:
                amount_paid = 0.0
            
            if not supplier_name:
                messagebox.showerror("Error", "Supplier name is required")
                return
                
            if not bill_no:
                messagebox.showerror("Error", "Bill number is required")
                return
                
            # Calculate total from the purchase tree
            total_purchase = 0.0
            items = []
            for child in purchase_tree.get_children():
                values = purchase_tree.item(child)['values']
                item_total = float(values[5])
                total_purchase += item_total
                items.append({
                    'brand': values[1],
                    'product': values[2],
                    'qty': float(values[3]),
                    'rate': float(values[4]),
                    'total': item_total
                })
                
            if not items:
                messagebox.showerror("Error", "No items in purchase")
                return
            
            # Calculate remaining amount
            remaining = max(0, total_purchase - amount_paid)
            
            # Save detailed items information
            Dialogs.save_purchase_items_details(bill_no, date, supplier_name, items)

            # Save to purchases.csv
            try:
                fieldnames = ['Date', 'Supplier', 'Phone', 'Bill No', 'Place', 'Site', 
                            'Payment Type', 'Items Count', 'Total Purchase', 'Paid', 'Remaining']
                
                file_exists = os.path.exists("purchases.csv")
                
                with open("purchases.csv", mode="a", newline="", encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    
                    if not file_exists:
                        writer.writeheader()
                    
                    purchase_data = {
                        'Date': date,
                        'Supplier': supplier_name,
                        'Phone': supplier_phone,
                        'Bill No': bill_no,
                        'Place': place,
                        'Site': site,
                        'Payment Type': payment_type,
                        'Items Count': str(len(items)),
                        'Total Purchase': f"{total_purchase:.2f}",
                        'Paid': f"{amount_paid:.2f}",
                        'Remaining': f"{remaining:.2f}"
                    }
                    
                    writer.writerow(purchase_data)
                
                # Update product stock
                for item in items:
                    for product in app.products:
                        if product.get('Brand', '') == item['brand'] and product.get('Product Name', '') == item['product']:
                            purchased = int(product.get('Purchased Stock', 0)) + int(item['qty'])
                            product['Purchased Stock'] = str(purchased)
                            product['Closing Stock'] = str(update_closing_stock(
                                int(product.get('Opening Stock', 0)),
                                purchased,
                                int(product.get('Sold Stock', 0))
                            ))
                            # Update purchase rate
                            product['Purchase Rate'] = f"{item['rate']:.2f}"
                            product['Purchase Date'] = date
                            break
                
                # Save updated products
                ProductModel.save_products(app.products)
                app.load_products()
                
                messagebox.showinfo("Success", f"Purchase saved successfully!\nTotal: ₹{total_purchase:.2f}\nPaid: ₹{amount_paid:.2f}\nRemaining: ₹{remaining:.2f}")
                
                # Close window
                purchase_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save purchase: {str(e)}")
        
        save_frame = tk.Frame(purchase_window)
        save_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(save_frame, text="Save Purchase", command=save_purchase).pack()
        
        # Initialize product list
        update_purchase_product_list()
    
    @staticmethod
    def save_purchase_items_details(bill_no, date, supplier_name, items):
        """Save detailed purchase items to a separate file"""
        try:
            items_filename = f"purchase_items_{bill_no}.csv"
            fieldnames = ['Bill No', 'Date', 'Supplier', 'Brand', 'Product', 'Quantity', 'Rate', 'Total']
            
            with open(items_filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in items:
                    writer.writerow({
                        'Bill No': bill_no,
                        'Date': date,
                        'Supplier': supplier_name,
                        'Brand': item['brand'],
                        'Product': item['product'],
                        'Quantity': f"{item['qty']:.2f}",
                        'Rate': f"{item['rate']:.2f}",
                        'Total': f"{item['total']:.2f}"
                    })
            
            print(f"Saved detailed items to: {items_filename}")
        except Exception as e:
            print(f"Error saving purchase items details: {e}")
    
    @staticmethod
    def create_sales_receipt_window(app):
        """Create sales receipt window"""
        from ..utils.file_operations import load_customers
        
        receipt_window = tk.Toplevel(app.root)
        receipt_window.title("Add Sales Receipt")
        receipt_window.geometry("800x500")
        
        # Customer selection
        tk.Label(receipt_window, text="Select Customer:").pack(pady=(10,0))
        sales_customer_combo = ttk.Combobox(receipt_window, width=40)
        sales_customer_combo.pack(pady=5)
        
        # Frame for displaying customer details
        details_frame = tk.Frame(receipt_window)
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Labels for customer details
        tk.Label(details_frame, text="Total Sales:").grid(row=0, column=0, sticky="w")
        total_amount_label = tk.Label(details_frame, text="0.00", font=("Arial", 10))
        total_amount_label.grid(row=0, column=1, sticky="w", padx=10)
        
        tk.Label(details_frame, text="Amount Paid:").grid(row=1, column=0, sticky="w")
        amount_paid_label = tk.Label(details_frame, text="0.00", font=("Arial", 10))
        amount_paid_label.grid(row=1, column=1, sticky="w", padx=10)
        
        tk.Label(details_frame, text="Remaining Amount:").grid(row=2, column=0, sticky="w")
        remaining_amount_label = tk.Label(details_frame, text="0.00", font=("Arial", 10))
        remaining_amount_label.grid(row=2, column=1, sticky="w", padx=10)
        
        # Payment mode frame
        payment_frame = tk.Frame(receipt_window)
        payment_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(payment_frame, text="Payment Mode:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Payment mode options
        mode_frame = tk.Frame(payment_frame)
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(mode_frame, text="Cash:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        cash_entry = tk.Entry(mode_frame, width=15)
        cash_entry.grid(row=0, column=1, padx=5, pady=2)
        cash_entry.insert(0, "0.00")
        
        tk.Label(mode_frame, text="Cheque:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        cheque_entry = tk.Entry(mode_frame, width=15)
        cheque_entry.grid(row=1, column=1, padx=5, pady=2)
        cheque_entry.insert(0, "0.00")
        
        tk.Label(mode_frame, text="Bank Transfer:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        bank_transfer_entry = tk.Entry(mode_frame, width=15)
        bank_transfer_entry.grid(row=2, column=1, padx=5, pady=2)
        bank_transfer_entry.insert(0, "0.00")
        
        # Amount received now
        tk.Label(payment_frame, text="Amount Received Now:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
        amount_received_now_entry = tk.Entry(payment_frame, font=("Arial", 10))
        amount_received_now_entry.pack(fill=tk.X, padx=10, pady=5)
        amount_received_now_entry.insert(0, "0.00")
        
        # Payment date
        tk.Label(payment_frame, text="Payment Date:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
        payment_date_entry = DateEntry(payment_frame, width=12, background='darkblue', 
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        payment_date_entry.pack(anchor="w", pady=5)
        
        def update_amount_received_now():
            """Auto-calculate total amount received when payment modes change"""
            try:
                cash = float(cash_entry.get() or 0)
                cheque = float(cheque_entry.get() or 0)
                bank_transfer = float(bank_transfer_entry.get() or 0)
                
                total_received = cash + cheque + bank_transfer
                amount_received_now_entry.delete(0, tk.END)
                amount_received_now_entry.insert(0, f"{total_received:.2f}")
            except ValueError:
                pass
        
        cash_entry.bind("<KeyRelease>", lambda e: update_amount_received_now())
        cheque_entry.bind("<KeyRelease>", lambda e: update_amount_received_now())
        bank_transfer_entry.bind("<KeyRelease>", lambda e: update_amount_received_now())
        
        def update_sales_receipt_details(event=None):
            """Update sales receipt details when customer is selected"""
            customer_name = sales_customer_combo.get()
            if not customer_name:
                return
            
            # Load customers
            customers = load_customers()
            
            # Find customer
            customer = None
            for c in customers:
                if c.get('Name', '') == customer_name:
                    customer = c
                    break
            
            if customer:
                # You would calculate totals from existing bills here
                # For now, just show customer info
                total_amount_label.config(text=f"Customer: {customer.get('Name', '')}")
        
        sales_customer_combo.bind("<<ComboboxSelected>>", update_sales_receipt_details)
        
        # Load customer suggestions
        customers = load_customers()
        sales_customer_combo['values'] = [c.get('Name', '') for c in customers if c.get('Name')]
        
        # Save button
        def save_sales_receipt():
            customer = sales_customer_combo.get()
            if not customer:
                messagebox.showerror("Error", "Please select a customer")
                return
                
            try:
                cash = float(cash_entry.get() or 0)
                cheque = float(cheque_entry.get() or 0)
                bank_transfer = float(bank_transfer_entry.get() or 0)
                amount_received_now = float(amount_received_now_entry.get() or 0)
                
                if amount_received_now <= 0:
                    messagebox.showerror("Error", "Amount received must be positive")
                    return
                    
                payment_date = payment_date_entry.get_date().strftime("%Y-%m-%d")
                
                # Calculate total payments
                total_payment = cash + cheque + bank_transfer
                
                if abs(total_payment - amount_received_now) > 0.01:
                    messagebox.showerror("Error", f"Sum of payment modes ({total_payment:.2f}) must equal amount received ({amount_received_now:.2f})")
                    return
                    
                # Save receipt
                fieldnames = ['Date', 'Customer', 'Amount Received', 'Cash', 'Cheque', 
                            'Bank Transfer', 'Total Sales', 'Initial Paid', 
                            'Total Paid', 'Remaining']
                
                file_exists = os.path.exists("sales_receipts.csv")
                try:
                    with open("sales_receipts.csv", mode="a", newline="", encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()
                            
                        writer.writerow({
                            'Date': payment_date,
                            'Customer': customer,
                            'Amount Received': f"{amount_received_now:.2f}",
                            'Cash': f"{cash:.2f}",
                            'Cheque': f"{cheque:.2f}",
                            'Bank Transfer': f"{bank_transfer:.2f}",
                            'Total Sales': "0.00",  # Would calculate from bills
                            'Initial Paid': "0.00",
                            'Total Paid': f"{amount_received_now:.2f}",
                            'Remaining': "0.00"
                        })
                    
                    messagebox.showinfo("Success", f"Sales receipt saved successfully!\n\nCustomer: {customer}\nAmount Received: ₹{amount_received_now:.2f}\nDate: {payment_date}")
                    
                    # Clear the form
                    sales_customer_combo.set('')
                    cash_entry.delete(0, tk.END)
                    cash_entry.insert(0, "0.00")
                    cheque_entry.delete(0, tk.END)
                    cheque_entry.insert(0, "0.00")
                    bank_transfer_entry.delete(0, tk.END)
                    bank_transfer_entry.insert(0, "0.00")
                    amount_received_now_entry.delete(0, tk.END)
                    amount_received_now_entry.insert(0, "0.00")
                    total_amount_label.config(text="0.00")
                    amount_paid_label.config(text="0.00")
                    remaining_amount_label.config(text="0.00")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")
                    return
                        
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numbers for amounts")
        
        tk.Button(receipt_window, text="Save Receipt", command=save_sales_receipt, 
                bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=20)