

# src/utils/__init__.py
"""
Utility functions
"""
from .calculations import (
    calculate_retail_rate, 
    update_closing_stock,
    calculate_gst_amount,
    calculate_total_with_gst
)
from .file_operations import (
    load_customers,
    save_customer_to_csv,
    get_purchase_bill_number,
    get_next_bill_number
)

__all__ = [
    'calculate_retail_rate',
    'update_closing_stock',
    'calculate_gst_amount',
    'calculate_total_with_gst',
    'load_customers',
    'save_customer_to_csv',
    'get_purchase_bill_number',
    'get_next_bill_number'
]