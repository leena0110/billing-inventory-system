import csv
import os
from datetime import datetime, timedelta
import webbrowser
from tkinter import messagebox

from .utils.calculations import update_closing_stock
from .utils.file_operations import load_customers, save_customer_to_csv
from .models.product import ProductModel

class BillingOperations:
    """Operations for billing and receipt generation"""
    
    def __init__(self, app):
        self.app = app
    
    def save_bill(self):
        """Save the current bill"""
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
                save_customer_to_csv(
                    self.app.customer_phone.get(), 
                    self.app.customer_name.get(),
                    self.app.place_var.get(),
                    self.app.site_var.get()
                )
            
            # Save updated products (with sold stock)
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
    
    def save_bill_after_receipt(self):
        """Save bill after generating receipt (without showing save dialog)"""
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
                
            # Save customer details if provided
            if self.app.customer_name.get() != "Cash Sale" and self.app.customer_phone.get():
                save_customer_to_csv(
                    self.app.customer_phone.get(), 
                    self.app.customer_name.get(),
                    self.app.place_var.get(),
                    self.app.site_var.get()
                )
            
            # Save updated products (with sold stock)
            if ProductModel.save_products(self.app.products):
                print("DEBUG: Products saved successfully after billing receipt!")
                # Reload products to ensure consistency
                self.app.load_products()
            else:
                print("DEBUG: FAILED to save products after billing receipt!")
            
            # Generate new bill number for next bill
            self.generate_and_set_bill_number()
            self.app.bill_items = []
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
    
    def get_receipt_text(self):
        """Generate receipt text for display or sharing"""
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
            receipt_text = self.get_receipt_text()
            
            # Create WhatsApp URL
            whatsapp_url = f"https://wa.me/91{phone}?text={receipt_text.replace(' ', '%20').replace('\n', '%0A')}"
            
            # Open in default browser
            webbrowser.open(whatsapp_url)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing phone number: {str(e)}")