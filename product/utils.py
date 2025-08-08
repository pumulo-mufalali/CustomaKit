"""
Utility functions for product management
"""
from datetime import datetime, timedelta
from django.db.models import Q, Count, Sum, Avg
from .models import Product, Order

def get_product_statistics():
    """
    Get comprehensive product statistics
    """
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Calculate total revenue
    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Get average order value
    avg_order_value = Order.objects.aggregate(
        avg=Avg('total_amount')
    )['avg'] or 0
    
    return {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value
    }

def get_product_analytics():
    """
    Get detailed product analytics
    """
    # Top selling products
    top_products = Product.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count')[:5]
    
    # Monthly sales analysis
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_orders = Order.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).count()
    
    monthly_revenue = Order.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    return {
        'top_products': list(top_products.values('name', 'order_count')),
        'monthly_orders': monthly_orders,
        'monthly_revenue': monthly_revenue
    }

def search_products(query):
    """
    Search products by name or description
    """
    return Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

def calculate_order_total(order_items):
    """
    Calculate total for order items
    """
    total = 0
    for item in order_items:
        total += item['quantity'] * item['price']
    return total

def validate_product_data(data):
    """
    Validate product data before saving
    """
    errors = []
    
    if not data.get('name'):
        errors.append('Product name is required')
    
    if data.get('price'):
        try:
            price = float(data['price'])
            if price <= 0:
                errors.append('Price must be greater than 0')
        except ValueError:
            errors.append('Price must be a valid number')
    
    if data.get('quantity'):
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                errors.append('Quantity cannot be negative')
        except ValueError:
            errors.append('Quantity must be a valid integer')
    
    return errors

def get_low_stock_products(threshold=10):
    """
    Get products with low stock
    """
    return Product.objects.filter(quantity__lte=threshold)

def get_recent_orders(days=7):
    """
    Get recent orders
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    return Order.objects.filter(created_at__gte=cutoff_date)

def export_product_data(format='csv'):
    """
    Export product data in specified format
    """
    products = Product.objects.all()
    
    if format == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Description', 'Price', 'Quantity', 'Created At'])
        
        for product in products:
            writer.writerow([
                product.name,
                product.description,
                product.price,
                product.quantity,
                product.created_at.strftime('%Y-%m-%d')
            ])
        
        return output.getvalue()
    
    return None

def generate_sales_report(start_date=None, end_date=None):
    """
    Generate comprehensive sales report
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    orders = Order.objects.filter(
        created_at__range=[start_date, end_date]
    )
    
    total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    
    # Daily sales breakdown
    daily_sales = orders.extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(
        daily_total=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('day')
    
    return {
        'period': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        },
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': total_sales / total_orders if total_orders > 0 else 0,
        'daily_sales': list(daily_sales)
    }
