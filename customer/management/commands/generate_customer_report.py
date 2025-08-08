"""
Management command to generate customer reports
"""
from django.core.management.base import BaseCommand
from customer.models import Customer
from customer.utils import get_customer_statistics, get_customer_analytics
from datetime import datetime, timedelta
import json

class Command(BaseCommand):
    help = 'Generate customer reports and statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='Output file path (default: customer_report_YYYYMMDD.json)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'text'],
            default='json',
            help='Report format (default: json)'
        )

    def handle(self, *args, **options):
        try:
            output_file = options['output']
            format_type = options['format']
            
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f'customer_report_{timestamp}.json'
            
            # Get statistics
            stats = get_customer_statistics()
            analytics = get_customer_analytics()
            
            # Additional analysis
            customers_by_source = Customer.objects.values('source').annotate(
                count=Customer.objects.model.objects.count()
            ).order_by('-count')
            
            recent_customers = Customer.objects.filter(
                created_at__gte=datetime.now() - timedelta(days=7)
            ).count()
            
            report_data = {
                'generated_at': datetime.now().isoformat(),
                'statistics': stats,
                'analytics': analytics,
                'customers_by_source': list(customers_by_source),
                'recent_customers_7_days': recent_customers,
                'summary': {
                    'total_customers': stats['total'],
                    'active_customers': stats['active'],
                    'inactive_customers': stats['inactive'],
                    'recent_customers': stats['recent'],
                    'monthly_growth': analytics['monthly_growth']
                }
            }
            
            if format_type == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, default=str)
            
            elif format_type == 'text':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("CUSTOMER REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"Total Customers: {stats['total']}\n")
                    f.write(f"Active Customers: {stats['active']}\n")
                    f.write(f"Inactive Customers: {stats['inactive']}\n")
                    f.write(f"Recent Customers (30 days): {stats['recent']}\n")
                    f.write(f"Monthly Growth: {analytics['monthly_growth']}\n\n")
                    
                    f.write("CUSTOMERS BY SOURCE:\n")
                    f.write("-" * 20 + "\n")
                    for source in customers_by_source:
                        f.write(f"{source['source']}: {source['count']}\n")
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully generated customer report: {output_file}'
                )
            )
            
            # Print summary to console
            self.stdout.write(f"\nCustomer Report Summary:")
            self.stdout.write(f"Total Customers: {stats['total']}")
            self.stdout.write(f"Active Customers: {stats['active']}")
            self.stdout.write(f"Recent Customers (30 days): {stats['recent']}")
            self.stdout.write(f"Monthly Growth: {analytics['monthly_growth']}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating customer report: {str(e)}')
            )
