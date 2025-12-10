# src/utils/calculations.py
def calculate_retail_rate(wholesale, margin):
    """Calculate retail rate from wholesale and margin"""
    return round(wholesale * (1 + margin / 100), 2)

def update_closing_stock(opening, purchased, sold=0):
    """Update closing stock"""
    return opening + purchased - sold

def calculate_gst_amount(amount, gst_percentage=18):
    """Calculate GST amount"""
    return round(amount * gst_percentage / 100, 2)

def calculate_total_with_gst(amount, include_gst=True, gst_percentage=18):
    """Calculate total amount with GST"""
    if include_gst:
        return round(amount * (1 + gst_percentage / 100), 2)
    return amount