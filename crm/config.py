"""
Application configuration settings
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application configuration
class AppConfig:
    """Application configuration class"""
    
    # Database settings
    DATABASE_CONFIG = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Cache settings
    CACHE_CONFIG = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    
    # Email settings
    EMAIL_CONFIG = {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'HOST': 'smtp.gmail.com',
        'PORT': 587,
        'USE_TLS': True,
        'USE_SSL': False,
    }
    
    # File upload settings
    UPLOAD_CONFIG = {
        'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
        'ALLOWED_EXTENSIONS': ['.jpg', '.jpeg', '.png', '.gif', '.pdf'],
        'UPLOAD_DIR': BASE_DIR / 'uploads',
    }
    
    # Pagination settings
    PAGINATION_CONFIG = {
        'DEFAULT_PAGE_SIZE': 20,
        'MAX_PAGE_SIZE': 100,
    }
    
    # API settings
    API_CONFIG = {
        'DEFAULT_PAGE_SIZE': 10,
        'MAX_PAGE_SIZE': 50,
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
        ],
    }
    
    # Security settings
    SECURITY_CONFIG = {
        'PASSWORD_MIN_LENGTH': 8,
        'PASSWORD_REQUIRE_UPPERCASE': True,
        'PASSWORD_REQUIRE_LOWERCASE': True,
        'PASSWORD_REQUIRE_NUMBERS': True,
        'PASSWORD_REQUIRE_SPECIAL_CHARS': True,
        'SESSION_TIMEOUT': 3600,  # 1 hour
        'MAX_LOGIN_ATTEMPTS': 5,
        'LOCKOUT_DURATION': 900,  # 15 minutes
    }
    
    # Notification settings
    NOTIFICATION_CONFIG = {
        'EMAIL_NOTIFICATIONS': True,
        'SMS_NOTIFICATIONS': False,
        'PUSH_NOTIFICATIONS': False,
        'DEFAULT_FROM_EMAIL': 'noreply@crm.com',
    }
    
    # Reporting settings
    REPORTING_CONFIG = {
        'DEFAULT_REPORT_FORMAT': 'pdf',
        'AVAILABLE_FORMATS': ['pdf', 'csv', 'excel', 'json'],
        'REPORT_STORAGE_PATH': BASE_DIR / 'reports',
        'AUTO_GENERATE_REPORTS': False,
        'REPORT_RETENTION_DAYS': 30,
    }
    
    # Analytics settings
    ANALYTICS_CONFIG = {
        'TRACK_USER_ACTIVITY': True,
        'TRACK_PAGE_VIEWS': True,
        'TRACK_SEARCH_QUERIES': True,
        'ANALYTICS_RETENTION_DAYS': 90,
    }
    
    # Backup settings
    BACKUP_CONFIG = {
        'AUTO_BACKUP': True,
        'BACKUP_FREQUENCY': 'daily',
        'BACKUP_RETENTION_DAYS': 30,
        'BACKUP_PATH': BASE_DIR / 'backups',
        'INCLUDE_MEDIA': True,
        'INCLUDE_DATABASE': True,
    }

# Environment-specific configurations
class DevelopmentConfig(AppConfig):
    """Development environment configuration"""
    
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    
    # Development-specific settings
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    LOGGING_LEVEL = 'DEBUG'
    
    # Development database
    DATABASE_CONFIG = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

class ProductionConfig(AppConfig):
    """Production environment configuration"""
    
    DEBUG = False
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    
    # Production-specific settings
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Production database (example with PostgreSQL)
    DATABASE_CONFIG = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'crm_db'),
            'USER': os.environ.get('DB_USER', 'crm_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Configuration factory
def get_config(environment='development'):
    """Get configuration based on environment"""
    if environment == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Utility functions for configuration
def validate_config(config):
    """Validate configuration settings"""
    errors = []
    
    # Check required settings
    required_settings = ['DATABASE_CONFIG', 'SECURITY_CONFIG']
    for setting in required_settings:
        if not hasattr(config, setting):
            errors.append(f"Missing required setting: {setting}")
    
    # Validate database configuration
    if hasattr(config, 'DATABASE_CONFIG'):
        db_config = config.DATABASE_CONFIG.get('default', {})
        if not db_config.get('ENGINE'):
            errors.append("Database engine not specified")
        if not db_config.get('NAME'):
            errors.append("Database name not specified")
    
    # Validate security settings
    if hasattr(config, 'SECURITY_CONFIG'):
        sec_config = config.SECURITY_CONFIG
        if sec_config.get('PASSWORD_MIN_LENGTH', 0) < 6:
            errors.append("Password minimum length should be at least 6 characters")
    
    return errors

def get_setting(config, key, default=None):
    """Get a configuration setting with fallback"""
    if hasattr(config, key):
        return getattr(config, key)
    return default

def update_config(config, updates):
    """Update configuration with new settings"""
    for key, value in updates.items():
        setattr(config, key, value)
    return config
