"""
Utility functions for account management
"""
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib.auth import authenticate
from .models import Profile

def get_user_statistics():
    """
    Get comprehensive user statistics
    """
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Users registered in last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_users = User.objects.filter(
        date_joined__gte=thirty_days_ago
    ).count()
    
    return {
        'total': total_users,
        'active': active_users,
        'recent': recent_users,
        'inactive': total_users - active_users
    }

def search_users(query):
    """
    Search users by username, email, or first/last name
    """
    return User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )

def validate_user_data(data):
    """
    Validate user registration data
    """
    errors = []
    
    if not data.get('username'):
        errors.append('Username is required')
    elif User.objects.filter(username=data['username']).exists():
        errors.append('Username already exists')
    
    if not data.get('email'):
        errors.append('Email is required')
    elif User.objects.filter(email=data['email']).exists():
        errors.append('Email already exists')
    
    if not data.get('password'):
        errors.append('Password is required')
    elif len(data['password']) < 8:
        errors.append('Password must be at least 8 characters')
    
    if data.get('password') != data.get('confirm_password'):
        errors.append('Passwords do not match')
    
    return errors

def authenticate_user(username, password):
    """
    Authenticate user with enhanced error handling
    """
    if not username or not password:
        return None, "Username and password are required"
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return None, "Invalid username or password"
    
    if not user.is_active:
        return None, "Account is deactivated"
    
    return user, None

def get_user_activity(user_id, days=30):
    """
    Get user activity for specified days
    """
    user = User.objects.get(id=user_id)
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # This would need to be customized based on your activity tracking
    # For now, we'll return basic user info
    return {
        'user': user.username,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
        'is_active': user.is_active
    }

def export_user_data(format='csv'):
    """
    Export user data in specified format
    """
    users = User.objects.all()
    
    if format == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Date Joined', 'Is Active'])
        
        for user in users:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.date_joined.strftime('%Y-%m-%d'),
                user.is_active
            ])
        
        return output.getvalue()
    
    return None

def get_user_permissions(user):
    """
    Get detailed user permissions
    """
    permissions = []
    
    if user.is_superuser:
        permissions.append('Superuser')
    
    if user.is_staff:
        permissions.append('Staff')
    
    # Add custom permissions based on your app logic
    if hasattr(user, 'profile'):
        if user.profile.role:
            permissions.append(f'Role: {user.profile.role}')
    
    return permissions

def update_user_profile(user_id, data):
    """
    Update user profile with validation
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Update basic user fields
        if data.get('first_name'):
            user.first_name = data['first_name']
        
        if data.get('last_name'):
            user.last_name = data['last_name']
        
        if data.get('email'):
            # Check if email is already taken by another user
            if User.objects.filter(email=data['email']).exclude(id=user_id).exists():
                return False, "Email already exists"
            user.email = data['email']
        
        user.save()
        
        # Update profile if it exists
        if hasattr(user, 'profile'):
            profile = user.profile
            if data.get('phone'):
                profile.phone = data['phone']
            if data.get('address'):
                profile.address = data['address']
            profile.save()
        
        return True, "Profile updated successfully"
    
    except User.DoesNotExist:
        return False, "User not found"
    except Exception as e:
        return False, f"Error updating profile: {str(e)}"

def get_user_analytics():
    """
    Get user analytics data
    """
    # Monthly user growth
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_users = User.objects.filter(
        date_joined__year=current_year,
        date_joined__month=current_month
    ).count()
    
    # User activity analysis
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    
    return {
        'monthly_growth': monthly_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'total_users': active_users + inactive_users
    }

def cleanup_inactive_users(days_inactive=90):
    """
    Mark users as inactive if they haven't logged in for specified days
    """
    cutoff_date = datetime.now() - timedelta(days=days_inactive)
    inactive_users = User.objects.filter(
        last_login__lt=cutoff_date,
        is_active=True
    )
    
    count = inactive_users.count()
    inactive_users.update(is_active=False)
    
    return count
