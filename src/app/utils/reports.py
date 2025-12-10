# src/app/utils/reports.py
import csv
import os
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
from tkcalendar import DateEntry

class ReportGenerator:
    """Generate various sales reports"""
    
    @staticmethod
    def generate_sales_report(app, report_type):
        """Generate sales report based on type"""
        # Get all bill files
        bill_files = [f for f in os.listdir() if f.startswith("bill_") and f.endswith(".csv")]
        
        if not bill_files:
            messagebox.showinfo("Info", "No bills found to generate report")
            return
            
        # Filter by date range based on report type
        today = datetime.now().date()
        date_range = None
        
        if report_type == "daily":
            date_range = (today, today)
            title = "Daily Sales Report"
        elif report_type == "fortnight":
            date_range = (today - timedelta(days=14), today)
            title = "Fortnight Sales Report"
        elif report_type == "monthly":
            first_day = today.replace(day=1)
            date_range = (first_day, today)
            title = "Monthly Sales Report"
        elif report_type == "custom":
            # Open date selection dialog
            date_window = tk.Toplevel(app.root)
            date_window.title("Select Date Range")
            
            tk.Label(date_window, text="From Date:").pack()
            from_date = DateEntry(date_window, width=12, background='darkblue', 
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            from_date.pack()
            
            tk.Label(date_window, text="To Date:").pack()
            to_date = DateEntry(date_window, width=12, background='darkblue', 
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            to_date.pack()
            
            def generate_with_dates():
                date_range = (from_date.get_date(), to_date.get_date())
                date_window.destroy()
                ReportGenerator._generate_report(bill_files, date_range, "Custom Date Sales Report")
            
            tk.Button(date_window, text="Generate Report", command=generate_with_dates).pack(pady=10)
            return
        
        ReportGenerator._generate_report(bill_files, date_range, title)
    
    @staticmethod
    def _generate_report(bill_files, date_range, title):
        """Generate report window with data"""
        report_window = tk.Toplevel()
        report_window.title(title)
        report_window.geometry("1000x600")
        
        # Treeview with scrollbars
        frame = tk.Frame(report_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_y = tk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        tree = ttk.Treeview(frame, columns=(
            "Bill No", "Date", "Customer", "Type", "Place", "Site", "Payment Type", "Include GST", "Amount"
        ), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        # Configure columns to align left
        tree.heading("Bill No", text="Bill No", anchor="w")
        tree.heading("Date", text="Date", anchor="w")
        tree.heading("Customer", text="Customer", anchor="w")
        tree.heading("Type", text="Type", anchor="w")
        tree.heading("Place", text="Place", anchor="w")
        tree.heading("Site", text="Site", anchor="w")
        tree.heading("Payment Type", text="Payment Type", anchor="w")
        tree.heading("Include GST", text="Include GST", anchor="w")
        tree.heading("Amount", text="Amount", anchor="w")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Bill No", width=100, anchor="w")
        tree.column("Date", width=150, anchor="w")
        tree.column("Customer", width=200, anchor="w")
        tree.column("Type", width=100, anchor="w")
        tree.column("Place", width=100, anchor="w")
        tree.column("Site", width=100, anchor="w")
        tree.column("Payment Type", width=100, anchor="w")
        tree.column("Include GST", width=100, anchor="w")
        tree.column("Amount", width=100, anchor="w")
        
        total_sales = 0
        bills_in_range = 0
        
        for bill_file in bill_files:
            try:
                with open(bill_file, mode="r", newline="", encoding='utf-8') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Skip header
                    bill_info = next(reader)  # Bill info row
                    
                    # Parse bill date
                    try:
                        bill_date_str = bill_info[1].split()[0]  # Get date part only
                        bill_date = datetime.strptime(bill_date_str, "%d/%m/%Y").date()
                    except:
                        continue  # Skip if date parsing fails
                    
                    # Check if bill is within date range
                    if date_range and not (date_range[0] <= bill_date <= date_range[1]):
                        continue
                    
                    # Find total amount
                    amount = 0
                    include_gst = False
                    payment_type = "Cash"
                    for row in reader:
                        if row and row[0] == "Total":
                            amount = float(row[-1])  # Last column is total
                        if row and row[0] == "Include GST":
                            include_gst = row[1].lower() == "yes"
                        if row and row[0] == "Payment Type":
                            payment_type = row[1]
                    
                    # Get place, site, and payment type if available
                    place = bill_info[5] if len(bill_info) > 5 else ""
                    site = bill_info[6] if len(bill_info) > 6 else ""
                    include_gst_flag = bill_info[8] if len(bill_info) > 8 else "No"
                    
                    tree.insert("", tk.END, values=(
                        bill_info[0],  # Bill No
                        bill_info[1],  # Date
                        bill_info[2],  # Customer
                        bill_info[4],  # Type
                        place,
                        site,
                        payment_type,
                        include_gst_flag,
                        f"{amount:.2f}"  # Amount
                    ))
                    
                    total_sales += amount
                    bills_in_range += 1
            except Exception as e:
                print(f"Error reading {bill_file}: {e}")
        
        if bills_in_range == 0:
            tree.insert("", tk.END, values=("No bills found in selected date range", "", "", "", "", "", "", "", ""))
        else:
            tree.insert("", tk.END, values=("", "", "", "", "", "", "", "TOTAL:", f"{total_sales:.2f}"))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Summary frame
        summary_frame = tk.Frame(report_window)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(summary_frame, text=f"Total Bills: {bills_in_range}", anchor="w").pack(side=tk.LEFT)
        tk.Label(summary_frame, text=f"Total Sales: {total_sales:.2f}", anchor="w").pack(side=tk.LEFT, padx=20)
        
        # Export button
        tk.Button(report_window, text="Export to CSV", 
                 command=lambda: ReportGenerator.export_report(tree)).pack(pady=5)
    
    @staticmethod
    def export_report(tree):
        """Export report to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save report as"
        )
        
        if not filename:
            return
            
        try:
            with open(filename, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                headers = []
                for col in tree["columns"]:
                    headers.append(tree.heading(col)["text"])
                writer.writerow(headers)
                
                # Write data
                for item in tree.get_children():
                    writer.writerow(tree.item(item)["values"])
            
            messagebox.showinfo("Success", f"Report saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {e}")