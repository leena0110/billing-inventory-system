# src/app/ui/components/place_site_suggestions.py

def get_place_suggestions(customers, current_text=""):
    """Get place suggestions from customers"""
    places = sorted(set(c.get('Place', '') for c in customers if c.get('Place', '')))
    places = [p for p in places if p]  # Remove empty strings
    
    if current_text:
        filtered = [p for p in places if current_text.lower() in p.lower()]
        return filtered
    return places

def get_site_suggestions(customers, current_text=""):
    """Get site suggestions from customers"""
    sites = sorted(set(c.get('Site', '') for c in customers if c.get('Site', '')))
    sites = [s for s in sites if s]  # Remove empty strings
    
    if current_text:
        filtered = [s for s in sites if current_text.lower() in s.lower()]
        return filtered
    return sites

def get_supplier_suggestions(purchases, current_text=""):
    """Get supplier suggestions from purchases"""
    if not purchases:
        return []
    
    suppliers = sorted(set(p.get('Supplier', '') for p in purchases if p.get('Supplier', '')))
    
    if current_text:
        filtered = [s for s in suppliers if current_text.lower() in s.lower()]
        return filtered
    return suppliers