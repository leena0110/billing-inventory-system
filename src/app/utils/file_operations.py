# src/utils/file_operations.py
import csv
import os
from datetime import datetime

def load_customers():
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

def save_customer_to_csv(phone, name, place="", site=""):
    """Save customer to CSV file"""
    if not phone or name == "Cash Sale":
        return
        
    # Check if customer already exists
    customers = load_customers()
    customer_exists = False
    for customer in customers:
        if customer["Phone"] == phone:
            # Update existing customer
            customer["Name"] = name
            customer["Place"] = place
            customer["Site"] = site
            customer_exists = True
            break
            
    if not customer_exists:
        # Add new customer
        customers.append({
            "Name": name,
            "Phone": phone,
            "Place": place,
            "Site": site
        })
    
    # Save all customers
    try:
        with open("customers.csv", mode="w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Phone", "Place", "Site"])
            writer.writeheader()
            writer.writerows(customers)
    except Exception as e:
        print(f"Failed to save customer: {str(e)}")

def get_purchase_bill_number():
    """Generate automatic bill number for purchases"""
    # Simple sequential numbering for purchases
    if not os.path.exists("last_purchase_bill.txt"):
        with open("last_purchase_bill.txt", "w") as f:
            f.write("1")
    
    with open("last_purchase_bill.txt", "r") as f:
        last_number = int(f.read().strip())
    
    next_number = last_number + 1
    
    with open("last_purchase_bill.txt", "w") as f:
        f.write(str(next_number))
    
    return f"P{next_number:04d}"  # P for Purchase

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