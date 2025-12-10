# src/models/product.py
import csv
import os
from datetime import datetime

class ProductModel:
    """Product data model and operations"""
    
    @staticmethod
    def load_products():
        """Load products from CSV file"""
        products = []
        if os.path.exists("products.csv"):
            try:
                with open("products.csv", mode="r", newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Ensure all required fields exist with proper defaults
                        required_fields = {
                            'Margin1 (%)': '0',
                            'Margin2 (%)': '0', 
                            'Opening Stock': '0',
                            'Purchased Stock': '0',
                            'Sold Stock': '0',
                            'Purchase Rate': '0',
                            'Purchase Date': datetime.now().strftime("%Y-%m-%d"),
                            'Modified Date': datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        for field, default in required_fields.items():
                            if field not in row or not row[field].strip():
                                row[field] = default
                        
                        # Calculate rates and closing stock
                        from ..utils.calculations import calculate_retail_rate, update_closing_stock
                        
                        try:
                            purchase_rate = float(row.get('Purchase Rate', 0))
                            margin1 = float(row.get('Margin1 (%)', 0))
                            wholesale_rate = round(purchase_rate * (1 + margin1 / 100), 2)
                            row['Wholesale Rate'] = f"{wholesale_rate:.2f}"
                            
                            margin2 = float(row.get('Margin2 (%)', 0))
                            retail_rate = calculate_retail_rate(wholesale_rate, margin2)
                            row['Retail Rate'] = f"{retail_rate:.2f}"
                            
                            opening = int(row.get('Opening Stock', 0))
                            purchased = int(row.get('Purchased Stock', 0))
                            sold = int(row.get('Sold Stock', 0))
                            row['Closing Stock'] = str(update_closing_stock(opening, purchased, sold))
                        except ValueError:
                            continue
                        
                        products.append(row)
                
                print(f"DEBUG: Successfully loaded {len(products)} products")
            except Exception as e:
                print(f"Failed to load products: {str(e)}")
        else:
            print("DEBUG: products.csv file does not exist")
        
        return products
    
    @staticmethod
    def save_products(products):
        """Save products to CSV file"""
        if not products:
            print("DEBUG: No products to save")
            return False
            
        fieldnames = [
            "Brand", "Product Name", "Purchase Date", "Purchase Rate", 
            "Margin1 (%)", "Wholesale Rate", "Margin2 (%)", "Retail Rate",
            "Opening Stock", "Purchased Stock", "Sold Stock", "Closing Stock", "Modified Date"
        ]
        
        try:
            # Create backup of existing file
            if os.path.exists("products.csv"):
                backup_name = f"products_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                os.rename("products.csv", backup_name)
                print(f"DEBUG: Created backup: {backup_name}")
                
            with open("products.csv", mode="w", newline="", encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            
            print("DEBUG: Products saved successfully to CSV")
            return True
        except Exception as e:
            print(f"DEBUG: Save products error: {str(e)}")
            return False