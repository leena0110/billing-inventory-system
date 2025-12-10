import csv
import os
from datetime import datetime

class BillModel:
    """Model for bill data management"""
    
    @staticmethod
    def get_next_bill_number():
        """Generate next bill number"""
        if not os.path.exists("last_bill.txt"):
            with open("last_bill.txt", "w") as f:
                f.write("1")  # starting bill number

        with open("last_bill.txt", "r") as f:
            last_number = int(f.read().strip())

        next_number = last_number + 1

        with open("last_bill.txt", "w") as f:
            f.write(str(next_number))

        return f"{next_number:04d}"  # Format with leading zeros
    
    @staticmethod
    def get_purchase_bill_number():
        """Generate purchase bill number"""
        if not os.path.exists("last_purchase_bill.txt"):
            with open("last_purchase_bill.txt", "w") as f:
                f.write("1")
        
        with open("last_purchase_bill.txt", "r") as f:
            last_number = int(f.read().strip())
        
        next_number = last_number + 1
        
        with open("last_purchase_bill.txt", "w") as f:
            f.write(str(next_number))
        
        return f"P{next_number:04d}"  # P for Purchase
    
    @staticmethod
    def save_bill_details(bill_no, date, customer_data, items, payment_type, include_gst, amount_paid):
        """Save bill details to CSV file"""
        filename = f"bill_{bill_no}.csv"
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Bill No", "Date", "Customer", "Phone", "Type", "Place", "Site", "Payment Type", "Include GST"])
                writer.writerow([
                    bill_no,
                    date,
                    customer_data.get("name", ""),
                    customer_data.get("phone", ""),
                    customer_data.get("type", "Retail"),
                    customer_data.get("place", ""),
                    customer_data.get("site", ""),
                    payment_type,
                    "Yes" if include_gst else "No"
                ])
                
                writer.writerow([])
                writer.writerow(["S.No", "Brand", "Product", "Qty", "Rate", "Amount"])
                
                for i, item in enumerate(items, 1):
                    writer.writerow([
                        i,
                        item.get("brand", ""),
                        item.get("name", ""),
                        item.get("qty", 0),
                        item.get("rate", 0),
                        item.get("amount", 0)
                    ])
                
                total = sum(item.get("amount", 0) for item in items)
                if include_gst:
                    total = total * 1.18  # Add 18% GST
                
                amount_paid_float = float(amount_paid or 0)
                remaining = max(0, total - amount_paid_float)
                
                writer.writerow([])
                writer.writerow(["Total", "", "", "", "", f"{total:.2f}"])
                writer.writerow(["Amount Paid", "", "", "", "", f"{amount_paid_float:.2f}"])
                writer.writerow(["Remaining Amount", "", "", "", "", f"{remaining:.2f}"])
            
            return True
        except Exception as e:
            print(f"Failed to save bill: {str(e)}")
            return False
    
    @staticmethod
    def get_receipt_text(bill_no, date, customer_data, items, payment_type, include_gst):
        """Generate receipt text for sharing"""
        taxable = sum(item.get('amount', 0) for item in items)
        
        if include_gst:
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
            f"Bill No: {bill_no}",
            f"Date: {date}",
            f"Customer: {customer_data.get('name', '')}",
            f"Phone: {customer_data.get('phone', '')}",
            f"Place: {customer_data.get('place', '')}",
            f"Site: {customer_data.get('site', '')}",
            f"Payment Type: {payment_type}",
            "",
            "Items Purchased:",
            "-" * 40
        ]
        
        for i, item in enumerate(items, 1):
            short_brand = item.get('brand', '')[:5] + ('...' if len(item.get('brand', '')) > 5 else '')
            receipt_lines.append(
                f"{i}. {short_brand} - {item.get('name', '')}"
            )
            receipt_lines.append(
                f"   Qty: {item.get('qty', 0)} x ₹{item.get('rate', 0)} = ₹{item.get('amount', 0)}"
            )
        
        receipt_lines.extend([
            "-" * 40,
            f"Subtotal: ₹{taxable:.2f}"
        ])
        
        if include_gst:
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