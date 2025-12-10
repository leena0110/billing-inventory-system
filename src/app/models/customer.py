import csv
import os

class CustomerModel:
    """Model for customer data management"""
    
    @staticmethod
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
    
    @staticmethod
    def save_customer(phone, name, place="", site=""):
        """Save or update customer data"""
        if not phone or name == "Cash Sale":
            return False
            
        # Load existing customers
        customers = CustomerModel.load_customers()
        customer_exists = False
        
        # Check if customer already exists
        for customer in customers:
            if customer.get("Phone") == phone:
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
            return True
        except Exception as e:
            print(f"Failed to save customer: {str(e)}")
            return False
    
    @staticmethod
    def get_customer_by_name(name):
        """Get customer by name"""
        customers = CustomerModel.load_customers()
        for customer in customers:
            if customer.get("Name") == name:
                return customer
        return None
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate and format phone number"""
        if not phone:
            return None
        
        # Remove all non-digit characters
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        if len(clean_phone) == 10:
            return clean_phone
        elif len(clean_phone) == 11 and clean_phone.startswith('0'):
            return clean_phone[1:]
        elif len(clean_phone) == 12 and clean_phone.startswith('91'):
            return clean_phone[2:]
        else:
            return None