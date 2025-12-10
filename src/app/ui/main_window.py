import tkinter as tk
from tkinter import ttk, messagebox
from ..ui.components.styled_widgets import StyledButton
from ..utils.file_operations import load_customers, save_customer_to_csv
from ..utils.calculations import update_closing_stock
from ..models.product import ProductModel
from ..config.colors import COLORS, FONTS


class MainWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.COLORS = app.COLORS
        self.FONTS = app.FONTS
        
        print("🔄 Creating MainWindow...")
        try:
            self.setup_ui()
            print("✅ MainWindow created and UI setup complete!")
        except Exception as e:
            print(f"❌ ERROR creating MainWindow: {e}")
            import traceback
            traceback.print_exc()
    
    
    def setup_ui(self):
        """EXACT same setup_ui method from your original BillingApp class"""
        print("🔄 Starting MainWindow.setup_ui()...")
        
        try:
            # Clear any existing widgets
            widget_count = len(self.master.winfo_children())
            print(f"📊 Clearing {widget_count} existing widgets...")
            for widget in self.master.winfo_children():
                widget.destroy()
            
            print("📊 Setting up main container...")
            # Main container with better spacing
            main_container = tk.Frame(self.master, bg=self.COLORS['background'])
            main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
            print("✅ Main container created")
            
            # Header with better styling
            header_frame = tk.Frame(main_container, bg=self.COLORS['primary'], relief='raised', bd=1)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            print("✅ Header frame created")
            
            tk.Label(header_frame, text=self.app.company["name"], 
                    font=("Arial", 18, "bold"), fg=self.COLORS['text_light'], 
                    bg=self.COLORS['primary']).pack(pady=5)
            print("✅ Company name label added")
            
            # Setup all sections
            print("📊 Setting up customer section...")
            self.setup_customer_section(main_container)
            
            print("📊 Setting up product selection...")
            self.setup_product_selection(main_container)
            
            print("📊 Setting up bill items section...")
            self.setup_bill_items_section(main_container)
            
            print("📊 Setting up controls section...")
            self.setup_controls_section(main_container)
            
            print("📊 Setting up amount section...")
            self.setup_amount_section(main_container)
            
            print("📊 Setting up action section...")
            self.setup_action_section(main_container)
            
            print("✅ All UI sections setup complete!")
            print(f"📊 Window title: {self.master.title()}")
            print(f"📊 Window size: {self.master.geometry()}")
            
            # Force update and show
            self.master.update()
            print("✅ Window updated and should be visible")
            
        except Exception as e:
            print(f"❌ ERROR in setup_ui: {e}")
            import traceback
            traceback.print_exc()
            # Show error to user
            messagebox.showerror("UI Setup Error", f"Failed to setup UI: {str(e)}")
        
        # We'll add more sections later (bill items, controls, etc.)
    def setup_customer_section(self, parent):
        """Customer information section from your original code"""
        # Customer and Bill Info Section
        info_section = tk.Frame(parent, bg=self.COLORS['background'])
        info_section.pack(fill=tk.X, pady=10)
        
        # Left column - Customer Info
        customer_frame = tk.LabelFrame(info_section, text=" Customer Information ", 
                                    font=("Arial", 10, "bold"), bg=self.COLORS['background'],
                                    relief='groove', bd=1)
        customer_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Customer name and phone in one row
        customer_row1 = tk.Frame(customer_frame, bg=self.COLORS['background'])
        customer_row1.pack(fill=tk.X, pady=5)
        
        tk.Label(customer_row1, text="Customer Name:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(10, 5))
        
        self.customer_name_combo = ttk.Combobox(customer_row1, textvariable=self.app.customer_name, width=25)
        self.customer_name_combo.pack(side=tk.LEFT, padx=5)
        self.customer_name_combo.bind("<KeyRelease>", self.update_customer_suggestions)
        self.customer_name_combo.bind("<<ComboboxSelected>>", self.auto_fill_customer)
        
        tk.Label(customer_row1, text="Phone No:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(20, 5))
        
        self.customer_phone_entry = tk.Entry(customer_row1, textvariable=self.app.customer_phone, width=20)
        self.customer_phone_entry.pack(side=tk.LEFT, padx=5)


        # ADD THIS AFTER phone entry (around line where you have customer_phone_entry)
        # Place and Site in second row
        customer_row2 = tk.Frame(customer_frame, bg=self.COLORS['background'])
        customer_row2.pack(fill=tk.X, pady=5)
        
        tk.Label(customer_row2, text="Place:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(10, 5))
        
        self.place_combo = ttk.Combobox(customer_row2, textvariable=self.app.place_var, width=20)
        self.place_combo.pack(side=tk.LEFT, padx=5)
        self.place_combo.bind("<KeyRelease>", self.update_place_suggestions)
        
        tk.Label(customer_row2, text="Site:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(20, 5))
        
        self.site_combo = ttk.Combobox(customer_row2, textvariable=self.app.site_var, width=20)
        self.site_combo.pack(side=tk.LEFT, padx=5)
        self.site_combo.bind("<KeyRelease>", self.update_site_suggestions)

                # Add Bill Info Frame (Right column)
        bill_frame = tk.LabelFrame(info_section, text=" Bill Information ", 
                                font=("Arial", 10, "bold"), bg=self.COLORS['background'],
                                relief='groove', bd=1)
        bill_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Bill number and date in one row
        bill_row1 = tk.Frame(bill_frame, bg=self.COLORS['background'])
        bill_row1.pack(fill=tk.X, pady=5)
        
        tk.Label(bill_row1, text="Bill No:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(10, 5))
        
        self.bill_entry = tk.Entry(bill_row1, textvariable=self.app.bill_no, width=12, 
                                state='readonly', font=("Arial", 9, "bold"))
        self.bill_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(bill_row1, text="Date:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT, padx=(20, 5))
        
        date_label = tk.Label(bill_row1, textvariable=self.app.current_date, 
                            font=("Arial", 9), bg=self.COLORS['background'])
        date_label.pack(side=tk.LEFT, padx=5)
        
        # Generate initial bill number
        self.generate_and_set_bill_number()
    
    # Just update the imports in the methods:
    def update_customer_suggestions(self, event=None):
        """Update customer suggestions"""
        try:
            from ...utils.file_operations import load_customers
            customers = load_customers()
        except ImportError:
            # Fallback if import fails
            customers = []
        
        search_term = self.app.customer_name.get().lower()
        filtered = [
            c.get('Name', '')
            for c in customers 
            if search_term in c.get('Name', '').lower()
        ]
        
        self.customer_name_combo['values'] = filtered
    
    def save_customer(self, phone, name, place="", site=""):
        """Save customer to file"""
        try:
            from ...utils.file_operations import save_customer_to_csv
            save_customer_to_csv(phone, name, place, site)
        except ImportError:
            print("Warning: Could not import save_customer_to_csv")
    
    def auto_fill_customer(self, event):
        """EXACT same as your original method"""
        selected_name = self.customer_name_combo.get()
        customers = load_customers()
        
        for customer in customers:
            if customer['Name'] == selected_name:
                self.app.customer_phone.set(customer['Phone'])
                self.app.place_var.set(customer.get('Place', ''))
                self.app.site_var.set(customer.get('Site', ''))
                break
    
    def setup_product_selection(self, parent):
        """Product Selection Section from your original code"""
        product_section = tk.LabelFrame(parent, text=" Product Selection ", 
                                    font=("Arial", 10, "bold"), bg=self.COLORS['background'],
                                    relief='groove', bd=1)
        product_section.pack(fill=tk.X, pady=10)
        
        product_frame = tk.Frame(product_section, bg=self.COLORS['background'])
        product_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Brand selection
        tk.Label(product_frame, text="Select Brand:", font=("Arial", 9), 
                bg=self.COLORS['background']).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.brand_combo = ttk.Combobox(product_frame, values=self.get_brands(), width=15)
        self.brand_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.brand_combo.bind("<<ComboboxSelected>>", lambda e: self.update_product_list())
        
        # Product selection
        tk.Label(product_frame, text="Select Product:", font=("Arial", 9), 
                bg=self.COLORS['background']).grid(row=0, column=2, sticky="w", padx=(20, 5))
        
        self.product_combo = ttk.Combobox(product_frame, width=20)
        self.product_combo.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.product_combo.bind("<<ComboboxSelected>>", self.on_product_select)
        
        # Quantity and controls
        tk.Label(product_frame, text="Qty:", font=("Arial", 9), 
                bg=self.COLORS['background']).grid(row=0, column=4, sticky="w", padx=(20, 5))
        
        qty_entry = tk.Entry(product_frame, textvariable=self.app.qty_var, width=8, justify='center')
        qty_entry.grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
        # Rate toggle button
        self.rate_btn = tk.Button(product_frame, text="Wholesale Rate (W)", 
                                command=self.toggle_rate,
                                bg=self.COLORS['accent'], fg=self.COLORS['text_light'],
                                font=("Arial", 9), width=15)
        self.rate_btn.grid(row=0, column=6, sticky="w", padx=10, pady=5)
        
        # Add item button
        add_btn = tk.Button(product_frame, text="Add Item", 
                        command=self.add_selected_item_dropdown, 
                        bg=self.COLORS['success'], fg=self.COLORS['text_light'],
                        font=("Arial", 9, "bold"), width=12)
        add_btn.grid(row=0, column=7, sticky="w", padx=5, pady=5)
    
    def get_brands(self):
        """Get unique brands from products"""
        return sorted(set(p["Brand"] for p in self.app.products))
    
    def update_product_list(self):
        """Update the product dropdown based on selected brand"""
        selected_brand = self.brand_combo.get()
        
        if selected_brand:
            products = [p['Product Name'] for p in self.app.products if p['Brand'] == selected_brand]
            self.product_combo['values'] = products
            if products:
                self.product_combo.set(products[0])
        else:
            self.product_combo['values'] = []
            self.product_combo.set('')
    
    def on_product_select(self, event=None):
        """When a product is selected"""
        # We'll implement this later
        pass
    
    def toggle_rate(self):
        """Toggle between wholesale and retail rates"""
        if self.app.bill_type.get() == "R":
            self.app.bill_type.set("W")
            self.rate_btn.config(text="Wholesale Rate (W)", bg="lightgreen")
        else:
            self.app.bill_type.set("R")
            self.rate_btn.config(text="Retail Rate (R)", bg="lightblue")
        # We'll update the bill display later
    
    def add_selected_item_dropdown(self):
        """Add item to bill from dropdown selection - EXACT same as your original"""
        try:
            product_name = self.product_combo.get()
            if not product_name:
                from tkinter import messagebox
                messagebox.showerror("Error", "Please select a product")
                return
                
            # Debug before any changes
            print(f"DEBUG: BEFORE adding to bill - Product: {product_name}")
            
            # Find the product
            product = None
            for p in self.app.products:
                if p["Product Name"] == product_name:
                    product = p
                    break
            
            if not product:
                from tkinter import messagebox
                messagebox.showerror("Error", "Product not found")
                return
            
            try:
                qty = float(self.app.qty_var.get())
                if qty <= 0:
                    from tkinter import messagebox
                    messagebox.showerror("Error", "Quantity must be positive")
                    return
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("Error", "Invalid quantity")
                return
            
            # Get current rate based on bill type
            if self.app.bill_type.get() == "W":
                rate = float(product.get('Wholesale Rate', 0))
            else:
                rate = float(product.get('Retail Rate', 0))
                
            amount = qty * rate
            
            # Add to bill items
            self.app.bill_items.append({
                "brand": product["Brand"],
                "name": product_name,
                "qty": qty,
                "rate": rate,
                "amount": amount
            })

            print(f"DEBUG: Added {qty} x {product_name} @ {rate} = {amount}")
            
            # Update stock in products (sold stock)
            stock_updated = False
            for p in self.app.products:
                if p['Product Name'] == product_name:
                    # Get current values
                    current_opening = int(p.get('Opening Stock', 0))
                    current_purchased = int(p.get('Purchased Stock', 0))
                    current_sold = int(p.get('Sold Stock', 0))
                    current_closing = int(p.get('Closing Stock', 0))
                    
                    print(f"DEBUG: Before sale update - O:{current_opening} P:{current_purchased} S:{current_sold} C:{current_closing}")
                    
                    # Add the billed quantity to sold stock (ACCUMULATE)
                    new_sold = current_sold + qty
                    p['Sold Stock'] = str(int(new_sold))
                    
                    # Recalculate closing stock
                    new_closing = current_opening + current_purchased - new_sold
                    p['Closing Stock'] = str(int(new_closing))
                    
                    print(f"DEBUG: After sale update - O:{current_opening} P:{current_purchased} S:{new_sold} C:{new_closing}")
                    stock_updated = True
                    break
            
            # Save updated products to CSV
            if stock_updated:
                print("DEBUG: Attempting to save products to CSV after adding to bill...")
                # We'll implement the save method later
                # For now, just print
                print("DEBUG: Products would be saved here")
            
            # Update the bill display
            self.update_bill()
            self.app.qty_var.set("1")  # Reset quantity to 1
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
            print(f"Error in add_selected_item: {e}")
            import traceback
            traceback.print_exc()

    def update_bill(self):
        """Update the bill items display - EXACT same as your original"""
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add all bill items
        for i, item in enumerate(self.app.bill_items, 1):
            # Display first 5 letters of brand name to save space
            short_brand = item['brand'][:5] + ('...' if len(item['brand']) > 5 else '')
            self.tree.insert("", tk.END, values=(
                i,
                short_brand,
                item["name"],
                f"{item['qty']:.2f}",
                f"{item['rate']:.2f}",
                f"{item['amount']:.2f}",
                "❌"
            ))
        
        # Update total
        self.update_total_display()

    def setup_bill_items_section(self, parent):
        """Bill Items Section from your original code"""
        items_section = tk.LabelFrame(parent, text=" Bill Items ", 
                                    font=("Arial", 10, "bold"), bg=self.COLORS['background'],
                                    relief='groove', bd=1)
        items_section.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(items_section, bg=self.COLORS['background'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("sno", "brand", "name", "qty", "rate", "amount", "delete"), 
                            show="headings", height=4, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading("sno", text="S.No")
        self.tree.heading("brand", text="Brand")
        self.tree.heading("name", text="Product")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("rate", text="Rate")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("delete", text="")
        
        self.tree.column("sno", width=50, anchor="center")
        self.tree.column("brand", width=100, anchor="w")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("qty", width=70, anchor="e")
        self.tree.column("rate", width=90, anchor="e")
        self.tree.column("amount", width=110, anchor="e")
        self.tree.column("delete", width=40, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.delete_item)
    
    def setup_controls_section(self, parent):
        """Controls Section from your original code"""
        controls_section = tk.Frame(parent, bg=self.COLORS['background'])
        controls_section.pack(fill=tk.X, pady=(5, 10))
        
        # Left side - Edit and Options
        left_controls = tk.Frame(controls_section, bg=self.COLORS['background'])
        left_controls.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Edit button
        edit_btn = tk.Button(left_controls, text="Edit Selected Item", 
                        command=self.edit_bill_item,
                        bg=self.COLORS['warning'], fg=self.COLORS['text_light'],
                        font=("Arial", 9), width=15)
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Payment type (Cash/Credit)
        payment_frame = tk.Frame(left_controls, bg=self.COLORS['background'])
        payment_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(payment_frame, text="Payment Type:", font=("Arial", 9), 
                bg=self.COLORS['background']).pack(side=tk.LEFT)
        
        cash_radio = tk.Radiobutton(payment_frame, text="Cash", variable=self.app.payment_type, 
                                value="Cash", font=("Arial", 9), bg=self.COLORS['background'])
        cash_radio.pack(side=tk.LEFT)
        cash_radio.select()
        
        credit_radio = tk.Radiobutton(payment_frame, text="Credit", variable=self.app.payment_type, 
                                    value="Credit", font=("Arial", 9), bg=self.COLORS['background'])
        credit_radio.pack(side=tk.LEFT)
        
        # GST checkbox
        gst_check = tk.Checkbutton(left_controls, text="Include GST", 
                                variable=self.app.include_gst, 
                                command=self.update_total_display,
                                font=("Arial", 9), bg=self.COLORS['background'])
        gst_check.pack(side=tk.LEFT, padx=10)
    
    def setup_amount_section(self, parent):
        """Amount information section"""
        right_controls = tk.Frame(parent, bg=self.COLORS['background'])
        right_controls.pack(side=tk.RIGHT)
        
        amount_frame = tk.Frame(right_controls, bg=self.COLORS['background'])
        amount_frame.pack()
        
        tk.Label(amount_frame, text="Amount Paid:", font=("Arial", 9), 
                bg=self.COLORS['background']).grid(row=0, column=0, sticky="e", padx=(0, 5))
        
        amount_paid_entry = tk.Entry(amount_frame, textvariable=self.app.amount_paid_var, 
                                width=12, font=("Arial", 9))
        amount_paid_entry.grid(row=0, column=1, padx=5)
        amount_paid_entry.insert(0, "0.00")
        
        tk.Label(amount_frame, text="Remaining Amount:", font=("Arial", 9), 
                bg=self.COLORS['background']).grid(row=0, column=2, sticky="e", padx=(10, 5))
        
        remaining_label = tk.Label(amount_frame, textvariable=self.app.remaining_amount_var, 
                                font=("Arial", 9, "bold"), bg=self.COLORS['background'],
                                fg=self.COLORS['danger'], width=10)
        remaining_label.grid(row=0, column=3, padx=5)
        self.app.remaining_amount_var.set("0.00")
        
        # Update remaining amount when amount paid changes
        self.app.amount_paid_var.trace_add("write", self.update_remaining_amount)
    
    def setup_action_section(self, parent):
        """Bottom Action Section with Total, Save Bill, and Generate Receipt"""
        action_section = tk.Frame(parent, bg=self.COLORS['light'], relief='raised', bd=1)
        action_section.pack(fill=tk.X, pady=(5, 0))
        
        # Total display on left
        total_frame = tk.Frame(action_section, bg=self.COLORS['primary'])
        total_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 20), pady=3)
        
        tk.Label(total_frame, text="TOTAL:", font=("Arial", 12, "bold"), 
                fg=self.COLORS['text_light'], bg=self.COLORS['primary']).pack(side=tk.LEFT, padx=5)
        
        self.total_label = tk.Label(total_frame, text="0.00", font=("Arial", 14, "bold"), 
                                fg=self.COLORS['text_light'], bg=self.COLORS['primary'])
        self.total_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Action buttons on right
        button_frame = tk.Frame(action_section, bg=self.COLORS['light'])
        button_frame.pack(side=tk.RIGHT, padx=10, pady=3)
        
        from ..ui.components.styled_widgets import StyledButton
        
        save_btn = StyledButton(button_frame, text="Save Bill", 
                            command=self.save_bill,
                            bg=self.COLORS['secondary'], fg=self.COLORS['text_light'],
                            font=("Arial", 10, "bold"), width=12, height=1)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        receipt_btn = StyledButton(button_frame, text="Generate Receipt", 
                                command=self.generate_receipt,
                                bg=self.COLORS['success'], fg=self.COLORS['text_light'],
                                font=("Arial", 10, "bold"), width=15, height=1)
        receipt_btn.pack(side=tk.LEFT, padx=5)
    
    def delete_item(self, event):
        """Delete item from bill - EXACT same as your original logic"""
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        
        if col == "#7":  # Delete column
            selected_index = self.tree.index(item)
            if 0 <= selected_index < len(self.app.bill_items):
                # Get the item being deleted
                deleted_item = self.app.bill_items[selected_index]
                
                # Update sold stock in products (reduce by deleted quantity)
                stock_updated = False
                for p in self.app.products:
                    if p['Product Name'] == deleted_item['name']:
                        sold = max(0, int(p.get('Sold Stock', 0)) - int(deleted_item['qty']))
                        p['Sold Stock'] = str(sold)
                        p['Closing Stock'] = str(update_closing_stock(
                            int(p.get('Opening Stock', 0)),
                            int(p.get('Purchased Stock', 0)),
                            sold
                        ))
                        stock_updated = True
                        print(f"DEBUG: Deleted item - {deleted_item['name']}: Reduced sold stock by {deleted_item['qty']}")
                        break
                
                # Remove from bill items
                del self.app.bill_items[selected_index]
                self.update_bill()
    
    def edit_bill_item(self):
        """Edit selected bill item"""
        print("Edit bill item - to be implemented")
    
    def update_total_display(self):
        """Update the total amount displayed based on GST inclusion"""
        total = sum(item["amount"] for item in self.app.bill_items)
        if self.app.include_gst.get():
            total = total * 1.18  # Add 18% GST (9% CGST + 9% SGST)
        self.total_label.config(text=f"{total:.2f}")
        self.update_remaining_amount()  # Also update remaining amount
    
    def update_remaining_amount(self, *args):
        try:
            total = sum(item["amount"] for item in self.app.bill_items)
            if self.app.include_gst.get():
                total = total * 1.18  # Add 18% GST (9% CGST + 9% SGST)
            
            amount_paid = float(self.app.amount_paid_var.get() or 0)
            remaining = max(0, total - amount_paid)
            self.app.remaining_amount_var.set(f"{remaining:.2f}")
        except ValueError:
            self.app.remaining_amount_var.set("0.00")
    
    def save_bill(self):
        """Save the current bill - EXACT same as your original"""
        from tkinter import messagebox
        import csv
        
        if not self.app.bill_items:
            messagebox.showerror("Error", "No items in bill to save")
            return
            
        # Generate bill number if not exists
        if not self.app.bill_no.get():
            self.generate_and_set_bill_number()
            
        filename = f"bill_{self.app.bill_no.get()}.csv"
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Bill No", "Date", "Customer", "Phone", "Type", "Place", "Site", "Payment Type", "Include GST"])
                writer.writerow([
                    self.app.bill_no.get(),
                    self.app.current_date.get(),
                    self.app.customer_name.get(),
                    self.app.customer_phone.get(),
                    "Wholesale" if self.app.bill_type.get() == "W" else "Retail",
                    self.app.place_var.get(),
                    self.app.site_var.get(),
                    self.app.payment_type.get(),
                    "Yes" if self.app.include_gst.get() else "No"
                ])
                
                writer.writerow([])
                writer.writerow(["S.No", "Brand", "Product", "Qty", "Rate", "Amount"])
                
                for i, item in enumerate(self.app.bill_items, 1):
                    writer.writerow([
                        i,
                        item["brand"],
                        item["name"],
                        item["qty"],
                        item["rate"],
                        item["amount"]
                    ])
                
                total = sum(item["amount"] for item in self.app.bill_items)
                if self.app.include_gst.get():
                    total = total * 1.18  # Add 18% GST
                
                amount_paid = float(self.app.amount_paid_var.get() or 0)
                remaining = max(0, total - amount_paid)
                
                writer.writerow([])
                writer.writerow(["Total", "", "", "", "", f"{total:.2f}"])
                writer.writerow(["Amount Paid", "", "", "", "", f"{amount_paid:.2f}"])
                writer.writerow(["Remaining Amount", "", "", "", "", f"{remaining:.2f}"])
            
            # Save customer details if provided
            if self.app.customer_name.get() != "Cash Sale" and self.app.customer_phone.get():
                from ..utils.file_operations import save_customer_to_csv
                save_customer_to_csv(
                    self.app.customer_phone.get(), 
                    self.app.customer_name.get(),
                    self.app.place_var.get(),
                    self.app.site_var.get()
                )
            
            # Save updated products (with sold stock)
            from ..models.product import ProductModel
            if ProductModel.save_products(self.app.products):
                print("DEBUG: Products saved successfully with sold stock updates")
                # Reload products to ensure consistency
                self.app.load_products()
            else:
                print("DEBUG: Failed to save products with sold stock")
            
            messagebox.showinfo("Success", f"Bill saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
    
    def generate_and_set_bill_number(self):
        """Generate automatic bill number"""
        import os
        
        # Simple sequential numbering
        if not os.path.exists("last_bill.txt"):
            with open("last_bill.txt", "w") as f:
                f.write("1")
        
        with open("last_bill.txt", "r") as f:
            last_number = int(f.read().strip())
        
        next_number = last_number + 1
        
        with open("last_bill.txt", "w") as f:
            f.write(str(next_number))
        
        bill_number = f"{next_number:04d}"  # Format with leading zeros
        self.app.bill_no.set(bill_number)
        
        # Also update bill entry if exists
        if hasattr(self, 'bill_entry') and self.bill_entry:
            self.bill_entry.configure(state='normal')
            self.bill_entry.delete(0, tk.END)
            self.bill_entry.insert(0, bill_number)
            self.bill_entry.configure(state='readonly')
    

    def generate_receipt(self):
        """Generate receipt - FULL implementation from your original code"""
        if not self.app.bill_items:
            messagebox.showerror("Error", "No items in bill")
            return
            
        taxable = sum(item["amount"] for item in self.app.bill_items)
        
        if self.app.include_gst.get():
            cgst = taxable * 0.09
            sgst = taxable * 0.09
            total = taxable + cgst + sgst
        else:
            cgst = 0
            sgst = 0
            total = taxable
        
        # Remove amount paid and remaining amount calculations for receipt
        # amount_paid = float(self.app.amount_paid_var.get() or 0)
        # remaining = max(0, total - amount_paid)
        
        receipt = [
            f"{self.app.company['name']:^50}",
            f"{self.app.company['address']:^50}",
            f"{'Phone: ' + self.app.company['phone']:^50}",
            f"{self.app.company['gstin']:^50}",
            "-"*50,
            f"{'Bill No: ' + self.app.bill_no.get():<25}{'Date: ' + self.app.current_date.get():>25}",
            f"{'Customer: ' + self.app.customer_name.get():<50}",
            f"{'Phone: ' + self.app.customer_phone.get():<50}",
            f"{'Place: ' + self.app.place_var.get():<25}{'Site: ' + self.app.site_var.get():>25}",
            f"{'Payment Type: ' + self.app.payment_type.get():<50}",
            "-"*50,
            f"{'S.No':<5}{'Brand':<10}{'Product':<20}{'Qty':>5}{'Amount':>10}",
            "-"*50
        ]
        
        for i, item in enumerate(self.app.bill_items, 1):
            short_brand = item['brand'][:5] + ('...' if len(item['brand']) > 5 else '')
            receipt.append(
                f"{i:<5}{short_brand:<10}{item['name'][:20]:<20}"
                f"{item['qty']:>5.2f}{item['amount']:>10.2f}"
            )
        
        receipt.extend(["-"*50])
        
        if self.app.include_gst.get():
            receipt.extend([
                f"{'Subtotal:':<40}{taxable:>10.2f}",
                f"{'CGST @9%:':<40}{cgst:>10.2f}",
                f"{'SGST @9%:':<40}{sgst:>10.2f}"
            ])
        
        # Only show total amount, remove amount paid and remaining amount
        receipt.extend([
            f"{'Total:':<40}{total:>10.2f}",
            "-"*50,
            f"{'Thank you for your business!':^50}",
            f"{'Please visit again!':^50}"
        ])
        
        # Show receipt in a new window
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title("Receipt")
        receipt_window.geometry("600x500")
        
        text_frame = tk.Frame(receipt_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, font=("Courier", 10), yscrollcommand=scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        text.insert(tk.END, "\n".join(receipt))
        text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(receipt_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Print button
        tk.Button(btn_frame, text="Print", 
                command=lambda: self.print_receipt("\n".join(receipt))).pack(side=tk.LEFT)
        
        # WhatsApp share button
        if self.app.customer_phone.get():
            tk.Button(btn_frame, text="Share via WhatsApp", 
                    command=self.share_via_whatsapp,
                    bg="#25D366", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Close button
        tk.Button(btn_frame, text="Close & Save Bill", 
                command=lambda: self.close_receipt_and_save(receipt_window)).pack(side=tk.RIGHT)

    def print_receipt(self, text):
        """Print receipt to file"""
        filename = f"receipt_{self.app.bill_no.get()}.txt"
        try:
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Receipt saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")

    def share_via_whatsapp(self):
        """Share receipt via WhatsApp"""
        phone = self.app.customer_phone.get().strip()
        
        if not phone:
            messagebox.showerror("Error", 
                "No phone number provided for WhatsApp sharing.\n\n"
                "Please enter a phone number for the customer.\n"
                "For Cash Sales, enter 'Cash' as customer name with a phone number.")
            return
        
        try:
            # Format phone number
            phone = ''.join(filter(str.isdigit, phone))
            
            if not phone:
                messagebox.showerror("Error", "Please enter a valid phone number")
                return
            
            # Remove leading 0 or 91
            if phone.startswith('91') and len(phone) > 10:
                phone = phone[2:]
            elif phone.startswith('0'):
                phone = phone[1:]
            
            # Ensure phone number has 10 digits
            if len(phone) != 10:
                messagebox.showerror("Error", "Please enter a valid 10-digit phone number")
                return
            
            # Get receipt text
            receipt_text = self.get_receipt_text_for_whatsapp()
            
            # Create WhatsApp URL
            whatsapp_url = f"https://wa.me/91{phone}?text={receipt_text.replace(' ', '%20').replace('\n', '%0A')}"
            
            # Open in default browser
            import webbrowser
            webbrowser.open(whatsapp_url)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing phone number: {str(e)}")

    def get_receipt_text_for_whatsapp(self):
        """Get receipt text formatted for WhatsApp"""
        taxable = sum(item['amount'] for item in self.app.bill_items)
        
        if self.app.include_gst.get():
            cgst = taxable * 0.09
            sgst = taxable * 0.09
            total = taxable + cgst + sgst
        else:
            cgst = 0
            sgst = 0
            total = taxable
        
        receipt_lines = [
            "RITE ELECTRICALS",
            "451A, Periyar Nagar, Opp Rajaji Statue",
            "Thirumangalam-625706",
            f"Bill No: {self.app.bill_no.get()}",
            f"Date: {self.app.current_date.get()}",
            f"Customer: {self.app.customer_name.get()}",
            f"Phone: {self.app.customer_phone.get()}",
            f"Place: {self.app.place_var.get()}",
            f"Site: {self.app.site_var.get()}",
            f"Payment Type: {self.app.payment_type.get()}",
            "",
            "Items Purchased:",
            "-" * 40
        ]
        
        for i, item in enumerate(self.app.bill_items, 1):
            short_brand = item['brand'][:5] + ('...' if len(item['brand']) > 5 else '')
            receipt_lines.append(
                f"{i}. {short_brand} - {item['name']}"
            )
            receipt_lines.append(
                f"   Qty: {item['qty']} x ₹{item['rate']} = ₹{item['amount']}"
            )
        
        receipt_lines.extend([
            "-" * 40,
            f"Subtotal: ₹{taxable:.2f}"
        ])
        
        if self.app.include_gst.get():
            receipt_lines.extend([
                f"CGST @9%: ₹{cgst:.2f}",
                f"SGST @9%: ₹{sgst:.2f}"
            ])
        
        receipt_lines.extend([
            f"Total: ₹{total:.2f}",
            "",
            "Thank you for your business!",
            "Please visit again!"
        ])
        
        return "\n".join(receipt_lines)

    def close_receipt_and_save(self, receipt_window):
        """Close receipt window and save bill"""
        # Save the bill
        self.save_bill_after_receipt()
        receipt_window.destroy()

    def save_bill_after_receipt(self):
        """Save bill after generating receipt"""
        # This should be in billing_operations.py, but for now implement here
        from ..models.product import ProductModel
        import csv
        
        if not self.app.bill_items:
            return
            
        filename = f"bill_{self.app.bill_no.get()}.csv"
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Bill No", "Date", "Customer", "Phone", "Type", "Place", "Site", "Payment Type", "Include GST"])
                writer.writerow([
                    self.app.bill_no.get(),
                    self.app.current_date.get(),
                    self.app.customer_name.get(),
                    self.app.customer_phone.get(),
                    "Wholesale" if self.app.bill_type.get() == "W" else "Retail",
                    self.app.place_var.get(),
                    self.app.site_var.get(),
                    self.app.payment_type.get(),
                    "Yes" if self.app.include_gst.get() else "No"
                ])
                
                writer.writerow([])
                writer.writerow(["S.No", "Brand", "Product", "Qty", "Rate", "Amount"])
                
                for i, item in enumerate(self.app.bill_items, 1):
                    writer.writerow([
                        i,
                        item["brand"],
                        item["name"],
                        item["qty"],
                        item["rate"],
                        item["amount"]
                    ])
                
                total = sum(item["amount"] for item in self.app.bill_items)
                if self.app.include_gst.get():
                    total = total * 1.18  # Add 18% GST
                
                writer.writerow([])
                writer.writerow(["Total", "", "", "", "", f"{total:.2f}"])
                
            # Save customer details
            from ..utils.file_operations import save_customer_to_csv
            if self.app.customer_name.get() != "Cash Sale" and self.app.customer_phone.get():
                save_customer_to_csv(
                    self.app.customer_phone.get(), 
                    self.app.customer_name.get(),
                    self.app.place_var.get(),
                    self.app.site_var.get()
                )
            
            # Save updated products
            if ProductModel.save_products(self.app.products):
                print("DEBUG: Products saved successfully after billing receipt!")
                # Reload products
                self.app.load_products()
            else:
                print("DEBUG: FAILED to save products after billing receipt!")
            
            # Generate new bill number for next bill
            self.generate_and_set_bill_number()
            self.app.bill_items = []
            self.update_bill()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
    
    def update_place_suggestions(self, event=None):
        """Update place suggestions"""
        from ..utils.file_operations import load_customers
        customers = load_customers()
        places = sorted(set(c.get('Place', '') for c in customers if c.get('Place', '')))
        places = [p for p in places if p]  # Remove empty strings
        
        current_text = self.app.place_var.get().lower()
        filtered = [p for p in places if current_text in p.lower()]
        
        if hasattr(self, 'place_combo'):
            self.place_combo['values'] = filtered

    def update_site_suggestions(self, event=None):
        """Update site suggestions"""
        from ..utils.file_operations import load_customers
        customers = load_customers()
        sites = sorted(set(c.get('Site', '') for c in customers if c.get('Site', '')))
        sites = [s for s in sites if s]  # Remove empty strings
        
        current_text = self.app.site_var.get().lower()
        filtered = [s for s in sites if current_text in s.lower()]
        
        if hasattr(self, 'site_combo'):
            self.site_combo['values'] = filtered