"""
Utility functions for customer management
"""
from datetime import datetime, timedelta
from django.db.models import Q, Count, Sum
from .models import Customer

def get_customer_statistics():
    """
    Get comprehensive customer statistics
    """
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    
    # Get customers created in last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_customers = Customer.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    return {
        'total': total_customers,
        'active': active_customers,
        'recent': recent_customers,
        'inactive': total_customers - active_customers
    }

def search_customers(query):
    """
    Search customers by name, email, or phone
    """
    return Customer.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(phone__icontains=query)
    )

def get_customer_analytics():
    """
    Get customer analytics data
    """
    # Monthly customer growth
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_customers = Customer.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).count()
    
    # Customer source analysis
    source_stats = Customer.objects.values('source').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return {
        'monthly_growth': monthly_customers,
        'source_distribution': list(source_stats)
    }

def validate_customer_data(data):
    """
    Validate customer data before saving
    """
    errors = []
    
    if not data.get('name'):
        errors.append('Name is required')
    
    if data.get('email'):
        # Check if email already exists
        if Customer.objects.filter(email=data['email']).exists():
            errors.append('Email already exists')
    
    if data.get('phone'):
        # Basic phone validation
        if len(data['phone']) < 10:
            errors.append('Phone number must be at least 10 digits')
    
    return errors

def export_customer_data(format='csv'):
    """
    Export customer data in specified format
    """
    customers = Customer.objects.all()
    
    if format == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Email', 'Phone', 'Source', 'Created At'])
        
        for customer in customers:
            writer.writerow([
                customer.name,
                customer.email,
                customer.phone,
                customer.source,
                customer.created_at.strftime('%Y-%m-%d')
            ])
        
        return output.getvalue()
    
    return None
