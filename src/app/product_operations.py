import csv
import os
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk

from .utils.calculations import calculate_retail_rate
from .utils.validators import safe_float_convert
from .models.product import ProductModel

class ProductOperations:
    """Operations for product management"""
    
    def __init__(self, app):
        self.app = app
    
    def get_current_product_stock(self, brand, product_name):
        """Get current stock values for a specific product"""
        for product in self.app.products:
            if product['Brand'].strip().lower() == brand.strip().lower() and \
            product['Product Name'].strip().lower() == product_name.strip().lower():
                return {
                    'opening_stock': int(product.get('Opening Stock', 0)),
                    'purchased_stock': int(product.get('Purchased Stock', 0)),
                    'sold_stock': int(product.get('Sold Stock', 0)),
                    'closing_stock': int(product.get('Closing Stock', 0))
                }
        return None
    
    def get_current_rate_for_product(self, product_name, current_date=None):
        """Get the current rate for a product considering future rate changes"""
        if current_date is None:
            current_date = datetime.now().date()
        
        # Check if there are any future rate changes for this product
        future_rate = None
        if os.path.exists("future_rate_changes.csv"):
            try:
                with open("future_rate_changes.csv", mode="r", encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row.get('Product Name') == product_name:
                            effective_date_str = row.get('Effective Date', '')
                            if effective_date_str:
                                try:
                                    effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d").date()
                                    if current_date >= effective_date:
                                        future_rate = {
                                            'purchase_rate': float(row.get('New Purchase Rate', 0)),
                                            'wholesale_rate': float(row.get('Wholesale Rate', 0)),
                                            'retail_rate': float(row.get('Retail Rate', 0)),
                                            'margin1': float(row.get('Margin1 (%)', 0)),
                                            'margin2': float(row.get('Margin2 (%)', 0))
                                        }
                                        break
                                except ValueError:
                                    continue
            except Exception as e:
                print(f"Error reading future rate changes: {e}")
        
        # If found an applicable future rate, use it
        if future_rate:
            return future_rate
        
        # Otherwise, use the current rate from products
        for product in self.app.products:
            if product['Product Name'] == product_name:
                return {
                    'purchase_rate': float(product.get('Purchase Rate', 0)),
                    'wholesale_rate': float(product.get('Wholesale Rate', 0)),
                    'retail_rate': float(product.get('Retail Rate', 0)),
                    'margin1': float(product.get('Margin1 (%)', 0)),
                    'margin2': float(product.get('Margin2 (%)', 0))
                }
        
        return None
    
    def check_and_apply_future_rate_changes(self):
        """Check and apply any future rate changes that have become effective"""
        if not os.path.exists("future_rate_changes.csv"):
            return
        
        try:
            today = datetime.now().date()
            future_changes = []
            changes_to_apply = []
            
            if os.path.getsize("future_rate_changes.csv") == 0:
                return
                
            with open("future_rate_changes.csv", mode="r", encoding='utf-8') as file:
                first_line = file.readline().strip()
                if not first_line:
                    return
                file.seek(0)
                
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    return
                    
                future_changes = list(reader)
            
            # Find changes that should be applied today
            remaining_changes = []
            for change in future_changes:
                effective_date_str = change.get('Effective Date', '')
                if not effective_date_str:
                    continue
                    
                try:
                    effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d").date()
                    if today >= effective_date:
                        changes_to_apply.append(change)
                    else:
                        remaining_changes.append(change)
                except ValueError:
                    continue
            
            # Apply the changes to products
            for change in changes_to_apply:
                product_name = change.get('Product Name', '')
                if not product_name:
                    continue
                    
                for p in self.app.products:
                    if p['Product Name'] == product_name:
                        p.update({
                            'Purchase Rate': change.get('New Purchase Rate', p['Purchase Rate']),
                            'Purchase Date': change.get('Effective Date', p['Purchase Date']),
                            'Margin1 (%)': change.get('Margin1 (%)', p['Margin1 (%)']),
                            'Wholesale Rate': change.get('Wholesale Rate', p['Wholesale Rate']),
                            'Margin2 (%)': change.get('Margin2 (%)', p['Margin2 (%)']),
                            'Retail Rate': change.get('Retail Rate', p['Retail Rate']),
                            'Modified Date': datetime.now().strftime("%Y-%m-%d")
                        })
                        break
            
            # Save updated products and future changes
            if changes_to_apply:
                ProductModel.save_products(self.app.products)
                
                # Update future changes file
                if remaining_changes:
                    with open("future_rate_changes.csv", mode="w", newline="", encoding='utf-8') as file:
                        fieldnames = [
                            'Product Name', 'New Purchase Rate', 'Effective Date', 
                            'Margin1 (%)', 'Wholesale Rate', 'Margin2 (%)', 
                            'Retail Rate', 'Modified Date'
                        ]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(remaining_changes)
                else:
                    os.remove("future_rate_changes.csv")
                    
                self.app.load_products()
                    
        except Exception as e:
            print(f"Error applying future rate changes: {e}")