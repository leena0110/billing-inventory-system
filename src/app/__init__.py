# Make app a package
from .billing_app import BillingApp
from .admin_features import AdminFeatures
from .billing_operations import BillingOperations
from .product_operations import ProductOperations

# src/app/__init__.py
"""
Application module for RITE ELECTRICALS Billing System
"""
from .billing_app import BillingApp
from .admin_features import AdminFeatures

__all__ = ['BillingApp', 'AdminFeatures']