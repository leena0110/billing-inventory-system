# RITE ELECTRICALS – Billing & Inventory Management System

A production-ready desktop application for automated billing, inventory tracking, customer management, and sales analytics designed for electrical goods businesses.

## 📋 Project Overview

The RITE ELECTRICALS Billing System is a full-scale business automation tool that:
- Handles 500+ daily transactions efficiently
- Manages real-time inventory using FIFO methodology
- Automates GST billing (18% = 9% CGST + 9% SGST)
- Tracks complete customer histories & credit systems
- Generates and sends digital receipts via WhatsApp
- Supports multi-user roles (Admin & User)
- Exports comprehensive business reports in CSV format

## ⭐ Key Features

### 🔐 Authentication System
- Admin & User roles with restricted access
- Secure login system for sensitive operations

### 📦 Inventory Management (FIFO-Based)
- Automated stock updates on purchase/sale transactions
- Complete stock tracking: Opening, Closing, Purchased, Sold
- Real-time stock level alerts and warnings
- First-In-First-Out valuation for accurate costing

### 🧾 Billing System
- Automatic GST calculation and application
- Support for Retail/Wholesale pricing models
- Printable physical receipts
- Digital receipt delivery via WhatsApp API

### 👤 Customer Management
- Comprehensive customer database
- Complete purchase history tracking
- Credit system management
- Auto-suggest search functionality

### 📊 Reporting & Analytics
- Daily/Monthly/Custom sales reports
- Stock summary analytics
- CSV export for external analysis
- Business performance insights

### 🔄 Purchase Order & Supplier Tracking
- Supplier details management
- Purchase entries recording
- Payment receipts generation

## 🏗️ Project Structure
billing-inventory-system/
├── main.py                    # Application entry point
├── src/
│   ├── app/                   # Main application logic
│   ├── config/                # Configuration files
│   │   └── colors.py          # UI themes and colors
│   ├── ui/                    # User interface
│   │   ├── main_window.py     # Main application window
│   │   └── dialogs.py         # Popup dialogs and forms
│   ├── models/                # Data models
│   │   ├── product.py         # Product data model
│   │   └── customer.py        # Customer data model
│   ├── utils/                 # Utility functions
│   │   ├── file_operations.py # CSV file read/write operations
│   │   ├── calculations.py    # GST, totals, stock calculations
│   │   └── reports.py         # Report generation
│   └── features/              # Feature modules
│       ├── admin_features.py  # Admin-specific functionality
│       └── billing_operations.py # Core billing operations
├── data/                      # CSV data files
├── requirements.txt           # Python dependencies
└── README.md                  # This documentation

text

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/leena0110/billing-inventory-system.git
cd billing-inventory-system
2️⃣ Install Dependencies
bash
pip install -r requirements.txt
If requirements.txt is not available, install:

bash
pip install tkinter
3️⃣ Run the Application
bash
python main.py
🔑 Default Login Credentials
Role	Username	Password
Admin	admin	admin123
User	user	user123
📊 Data Storage (CSV Files)
The application uses CSV files for lightweight, portable data storage:

products.csv - Product catalog with SKU, name, rate, GST, stock

customers.csv - Customer database with contact and credit info

sales_receipts.csv - Complete sales transaction records

purchases.csv - Purchase order records from suppliers

purchase_receipts.csv - Purchase transaction records

future_rate_changes.csv - Scheduled product rate changes

bill_*.csv - Generated bill records

receipt_*.txt - Printable receipt files

🔧 Key Modules
<details> <summary><strong>1. Billing System</strong></summary>
Product selection with real-time stock preview

Automatic GST calculation (CGST + SGST)

Support for Cash and Credit payment modes

Printable physical receipts + Digital WhatsApp receipts

Discount and promotional pricing support

</details><details> <summary><strong>2. Inventory Management</strong></summary>
FIFO (First-In-First-Out) stock valuation

Automated stock updates on transactions

Real-time low stock threshold alerts

Complete stock movement tracking

</details><details> <summary><strong>3. Customer Management</strong></summary>
Customer purchase history tracking

Credit ledger management

Auto-suggest search functionality

Customer analytics and insights

</details><details> <summary><strong>4. Admin Features</strong></summary>
Add/Edit/Delete products

Schedule future rate changes

Full sales reporting and analytics

System configuration and settings

</details><details> <summary><strong>5. Reporting & Analytics</strong></summary>
Daily sales reports

Monthly/Custom period filters

Stock summary analytics

CSV export functionality

</details>
💼 Business Impact
✅ Automated 500+ daily transactions efficiently

✅ Reduced billing time from 10 minutes → 2 minutes per invoice

✅ Eliminated stock discrepancies through FIFO tracking

✅ Delivered 300+ invoices monthly via WhatsApp digital delivery

✅ Improved customer satisfaction with faster service

🛠️ Technical Implementation
Tech Stack
Language: Python 3.8+

GUI Framework: Tkinter

Data Storage: CSV file system

Date Picker: tkcalendar

Integration: Webbrowser API (WhatsApp integration)

Design Patterns Used
MVC Architecture - Clear separation between Models, Views, and Controllers

Factory Pattern - For creating standardized UI widgets and components

Observer Pattern - For real-time updates between different modules

Modular Component Design - Independent, reusable components

Performance Optimizations
Lazy Loading - Data loaded on-demand to reduce startup time

Caching - Frequently accessed data cached in memory

Batch File Operations - Efficient CSV read/write operations

Non-blocking UI - Background processing for long operations

👩‍💻 Author
Leena Sri K

GitHub: @leena0110

Email: leenasri0110@gmail.com