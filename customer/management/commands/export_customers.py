"""
Management command to export customer data
"""
from django.core.management.base import BaseCommand
from customer.models import Customer
from customer.utils import export_customer_data
import csv
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Export customer data to CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='Output file path (default: customers_export_YYYYMMDD.csv)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['csv', 'json'],
            default='csv',
            help='Export format (default: csv)'
        )

    def handle(self, *args, **options):
        try:
            output_file = options['output']
            format_type = options['format']
            
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f'customers_export_{timestamp}.csv'
            
            # Get customer data
            customers = Customer.objects.all()
            
            if format_type == 'csv':
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Name', 'Email', 'Phone', 'Source', 'Created At', 'Is Active']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for customer in customers:
                        writer.writerow({
                            'Name': customer.name,
                            'Email': customer.email,
                            'Phone': customer.phone,
                            'Source': customer.source,
                            'Created At': customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'Is Active': customer.is_active
                        })
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully exported {customers.count()} customers to {output_file}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error exporting customers: {str(e)}')
            )
