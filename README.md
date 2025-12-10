RITE ELECTRICALS – Billing & Inventory Management System








A production-ready desktop application for automated billing, inventory tracking, customer management, and sales analytics designed for electrical goods businesses.

📋 Project Overview

The RITE ELECTRICALS Billing System is a full-scale business automation tool that:

Handles 500+ daily transactions

Manages real-time inventory using FIFO

Automates GST billing (18% = 9% CGST + 9% SGST)

Tracks customer histories & credit

Generates digital receipts via WhatsApp

Supports admin & user roles

Exports reports in CSV

⭐ Key Features
🔐 Authentication

Admin & User roles

Restricted access for sensitive operations

📦 Inventory Management (FIFO-Based)

Auto updates on purchase/sale

Opening, closing, purchased, sold stock

Stock level alerts

🧾 Billing System

GST auto-calculation

Retail/Wholesale pricing

Printable receipts

Digital receipts via WhatsApp

👤 Customer Management

Customer database

Full purchase history

Credit tracking

📊 Reporting

Daily / Monthly / Custom sales reports

Stock summary analytics

CSV export

🔄 Purchase Order + Supplier Tracking

Supplier details

Purchase entries

Payment receipts

🏗️ Project Structure
src/
├── app/
│   ├── main.py                # Application entry point
│   ├── config/
│   │   └── colors.py          # UI themes
│   ├── ui/
│   │   ├── main_window.py     # Main UI
│   │   └── dialogs.py         # Popup dialogs
│   ├── models/
│   │   ├── product.py         # Product model
│   │   └── customer.py        # Customer model
│   ├── utils/
│   │   ├── file_operations.py # CSV interactions
│   │   ├── calculations.py    # GST, totals, stock logic
│   │   └── reports.py         # CSV report generation
│   └── features/
│       ├── admin_features.py  
│       └── billing_operations.py

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/rite-electricals-billing-system.git
cd rite-electricals-billing-system

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Application
python main.py

🔑 Default Login Credentials
Role	Username	Password
Admin	admin	admin123
User	user	user123
📊 Data Storage (CSV Files Used)

products.csv

customers.csv

sales_receipts.csv

purchases.csv

purchase_receipts.csv

future_rate_changes.csv

bill_*.csv

receipt_*.txt

🔧 Key Modules (Summary)
<details> <summary><strong>1. Billing System</strong></summary>

Product selection with stock preview

GST auto-calculation

Cash/Credit payment modes

Printable + WhatsApp receipts

</details> <details> <summary><strong>2. Inventory Management</strong></summary>

FIFO stock valuation

Automated stock updates

Real-time threshold alerts

</details> <details> <summary><strong>3. Customer Management</strong></summary>

Purchase history

Credit ledger

Auto-suggest search

</details> <details> <summary><strong>4. Admin Features</strong></summary>

Add/Edit/Delete products

Schedule rate changes

Full sales reporting

</details> <details> <summary><strong>5. Reporting & Analytics</strong></summary>

Daily reports

Monthly/Custom filters

CSV export

</details>
💼 Business Impact

✔ Automated 500+ daily transactions
✔ Cut billing time from 10 minutes → 2 minutes
✔ Eliminated stock discrepancies
✔ Delivered 300+ invoices monthly via WhatsApp
✔ Improved customer satisfaction

🛠️ Technical Implementation
Tech Stack

Python 3.8+

Tkinter GUI

CSV Storage

tkcalendar (date picker)

Webbrowser API (WhatsApp integration)

Design Patterns Used

MVC Architecture

Factory Pattern (widgets)

Observer Pattern

Modular component design

Performance Optimizations

Lazy loading

Caching

Batch file operations

Non-blocking UI