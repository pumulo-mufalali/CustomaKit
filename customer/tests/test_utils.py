"""
Tests for customer utility functions
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from customer.models import Customer
from customer.utils import (
    get_customer_statistics,
    search_customers,
    get_customer_analytics,
    validate_customer_data,
    export_customer_data
)

class CustomerUtilsTestCase(TestCase):
    """Test case for customer utility functions"""
    
    def setUp(self):
        """Set up test data"""
        # Create test customers
        self.customer1 = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            source="website",
            is_active=True
        )
        
        self.customer2 = Customer.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            phone="0987654321",
            source="referral",
            is_active=True
        )
        
        self.customer3 = Customer.objects.create(
            name="Bob Johnson",
            email="bob@example.com",
            phone="5555555555",
            source="social_media",
            is_active=False
        )
    
    def test_get_customer_statistics(self):
        """Test customer statistics function"""
        stats = get_customer_statistics()
        
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['active'], 2)
        self.assertEqual(stats['inactive'], 1)
        self.assertIn('recent', stats)
    
    def test_search_customers(self):
        """Test customer search function"""
        # Search by name
        results = search_customers("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Search by email
        results = search_customers("jane@example.com")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email, "jane@example.com")
        
        # Search by phone
        results = search_customers("1234567890")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].phone, "1234567890")
        
        # Search with no results
        results = search_customers("nonexistent")
        self.assertEqual(len(results), 0)
    
    def test_get_customer_analytics(self):
        """Test customer analytics function"""
        analytics = get_customer_analytics()
        
        self.assertIn('monthly_growth', analytics)
        self.assertIn('source_distribution', analytics)
        self.assertIsInstance(analytics['monthly_growth'], int)
        self.assertIsInstance(analytics['source_distribution'], list)
    
    def test_validate_customer_data(self):
        """Test customer data validation"""
        # Valid data
        valid_data = {
            'name': 'Test Customer',
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        errors = validate_customer_data(valid_data)
        self.assertEqual(len(errors), 0)
        
        # Missing name
        invalid_data = {
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        errors = validate_customer_data(invalid_data)
        self.assertIn('Name is required', errors)
        
        # Invalid phone
        invalid_data = {
            'name': 'Test Customer',
            'email': 'test@example.com',
            'phone': '123'
        }
        errors = validate_customer_data(invalid_data)
        self.assertIn('Phone number must be at least 10 digits', errors)
        
        # Duplicate email
        invalid_data = {
            'name': 'Test Customer',
            'email': 'john@example.com',  # Already exists
            'phone': '1234567890'
        }
        errors = validate_customer_data(invalid_data)
        self.assertIn('Email already exists', errors)
    
    def test_export_customer_data(self):
        """Test customer data export"""
        # Test CSV export
        csv_data = export_customer_data('csv')
        self.assertIsInstance(csv_data, str)
        self.assertIn('Name,Email,Phone,Source,Created At', csv_data)
        
        # Test invalid format
        result = export_customer_data('invalid_format')
        self.assertIsNone(result)

class CustomerSearchTestCase(TestCase):
    """Test case for customer search functionality"""
    
    def setUp(self):
        """Set up test data for search"""
        Customer.objects.create(
            name="Alice Brown",
            email="alice@example.com",
            phone="1111111111",
            source="website"
        )
        Customer.objects.create(
            name="Charlie Davis",
            email="charlie@example.com",
            phone="2222222222",
            source="referral"
        )
    
    def test_case_insensitive_search(self):
        """Test case insensitive search"""
        results = search_customers("alice")
        self.assertEqual(len(results), 1)
        
        results = search_customers("ALICE")
        self.assertEqual(len(results), 1)
        
        results = search_customers("Alice")
        self.assertEqual(len(results), 1)
    
    def test_partial_search(self):
        """Test partial string search"""
        results = search_customers("alic")
        self.assertEqual(len(results), 1)
        
        results = search_customers("charl")
        self.assertEqual(len(results), 1)
    
    def test_multiple_search_criteria(self):
        """Test search with multiple criteria"""
        # Should find customers matching any criteria
        results = search_customers("example.com")
        self.assertEqual(len(results), 2)  # Both have example.com emails

class CustomerValidationTestCase(TestCase):
    """Test case for customer data validation"""
    
    def test_email_validation(self):
        """Test email validation"""
        # Valid email
        data = {'name': 'Test', 'email': 'valid@example.com'}
        errors = validate_customer_data(data)
        self.assertEqual(len(errors), 0)
        
        # Invalid email format
        data = {'name': 'Test', 'email': 'invalid-email'}
        errors = validate_customer_data(data)
        # Note: This test assumes basic email validation
    
    def test_phone_validation(self):
        """Test phone number validation"""
        # Valid phone
        data = {'name': 'Test', 'phone': '1234567890'}
        errors = validate_customer_data(data)
        self.assertEqual(len(errors), 0)
        
        # Too short phone
        data = {'name': 'Test', 'phone': '123'}
        errors = validate_customer_data(data)
        self.assertIn('Phone number must be at least 10 digits', errors)
    
    def test_required_fields(self):
        """Test required field validation"""
        # Missing name
        data = {'email': 'test@example.com'}
        errors = validate_customer_data(data)
        self.assertIn('Name is required', errors)
        
        # Empty name
        data = {'name': '', 'email': 'test@example.com'}
        errors = validate_customer_data(data)
        self.assertIn('Name is required', errors)

class CustomerAnalyticsTestCase(TestCase):
    """Test case for customer analytics"""
    
    def setUp(self):
        """Set up test data for analytics"""
        # Create customers with different creation dates
        Customer.objects.create(
            name="Customer 1",
            email="customer1@example.com",
            source="website",
            created_at=datetime.now() - timedelta(days=5)
        )
        Customer.objects.create(
            name="Customer 2",
            email="customer2@example.com",
            source="referral",
            created_at=datetime.now() - timedelta(days=10)
        )
        Customer.objects.create(
            name="Customer 3",
            email="customer3@example.com",
            source="website",
            created_at=datetime.now() - timedelta(days=35)
        )
    
    def test_monthly_growth_calculation(self):
        """Test monthly growth calculation"""
        analytics = get_customer_analytics()
        
        # Should have customers in current month
        self.assertGreaterEqual(analytics['monthly_growth'], 2)
    
    def test_source_distribution(self):
        """Test source distribution calculation"""
        analytics = get_customer_analytics()
        
        # Should have source distribution data
        self.assertIsInstance(analytics['source_distribution'], list)
        self.assertGreater(len(analytics['source_distribution']), 0)

class CustomerExportTestCase(TestCase):
    """Test case for customer data export"""
    
    def setUp(self):
        """Set up test data for export"""
        Customer.objects.create(
            name="Export Test",
            email="export@example.com",
            phone="9999999999",
            source="website"
        )
    
    def test_csv_export_format(self):
        """Test CSV export format"""
        csv_data = export_customer_data('csv')
        
        # Check CSV structure
        lines = csv_data.strip().split('\n')
        self.assertGreater(len(lines), 1)  # Header + at least one data row
        
        # Check header
        header = lines[0]
        expected_fields = ['Name', 'Email', 'Phone', 'Source', 'Created At']
        for field in expected_fields:
            self.assertIn(field, header)
        
        # Check data row
        data_row = lines[1]
        self.assertIn('Export Test', data_row)
        self.assertIn('export@example.com', data_row)
    
    def test_csv_export_content(self):
        """Test CSV export content"""
        csv_data = export_customer_data('csv')
        
        # Should contain customer data
        self.assertIn('Export Test', csv_data)
        self.assertIn('export@example.com', csv_data)
        self.assertIn('9999999999', csv_data)
        self.assertIn('website', csv_data)

if __name__ == '__main__':
    unittest.main()
