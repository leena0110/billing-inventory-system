def safe_float_convert(value, default=0.0):
    """Safely convert value to float, handling None, empty strings, and 'None' strings"""
    if value is None:
        return default
    if isinstance(value, str):
        if value.strip() == '' or value.strip().lower() == 'none':
            return default
        # Remove currency symbols if present
        value = value.replace('₹', '').replace('$', '').replace(',', '').strip()
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

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

def validate_quantity(qty_str):
    """Validate quantity input"""
    try:
        qty = float(qty_str)
        if qty <= 0:
            return None, "Quantity must be positive"
        return qty, None
    except ValueError:
        return None, "Invalid quantity format"

def validate_rate(rate_str):
    """Validate rate input"""
    try:
        rate = float(rate_str)
        if rate < 0:
            return None, "Rate must be positive"
        return rate, None
    except ValueError:
        return None, "Invalid rate format"