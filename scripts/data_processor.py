"""
Data processing utilities for CRM system
"""
import csv
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Main data processing class"""
    
    def __init__(self):
        self.processed_data = {}
        self.statistics = {}
    
    def process_customer_data(self, data: List[Dict]) -> Dict[str, Any]:
        """
        Process customer data and generate insights
        """
        try:
            df = pd.DataFrame(data)
            
            # Basic statistics
            total_customers = len(df)
            active_customers = len(df[df.get('is_active', True) == True])
            
            # Source analysis
            source_counts = df['source'].value_counts().to_dict()
            
            # Date analysis
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['month'] = df['created_at'].dt.month
                df['year'] = df['created_at'].dt.year
                
                monthly_growth = df.groupby(['year', 'month']).size().to_dict()
                recent_customers = len(df[df['created_at'] >= datetime.now() - timedelta(days=30)])
            else:
                monthly_growth = {}
                recent_customers = 0
            
            # Email analysis
            email_domains = df['email'].str.split('@').str[1].value_counts().head(10).to_dict()
            
            processed_data = {
                'total_customers': total_customers,
                'active_customers': active_customers,
                'inactive_customers': total_customers - active_customers,
                'source_distribution': source_counts,
                'monthly_growth': monthly_growth,
                'recent_customers': recent_customers,
                'top_email_domains': email_domains,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            self.processed_data['customers'] = processed_data
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing customer data: {str(e)}")
            return {}
    
    def process_product_data(self, data: List[Dict]) -> Dict[str, Any]:
        """
        Process product data and generate insights
        """
        try:
            df = pd.DataFrame(data)
            
            # Basic statistics
            total_products = len(df)
            total_value = df['price'].sum() if 'price' in df.columns else 0
            avg_price = df['price'].mean() if 'price' in df.columns else 0
            
            # Stock analysis
            if 'quantity' in df.columns:
                low_stock = len(df[df['quantity'] <= 10])
                out_of_stock = len(df[df['quantity'] == 0])
                total_stock_value = (df['price'] * df['quantity']).sum()
            else:
                low_stock = 0
                out_of_stock = 0
                total_stock_value = 0
            
            # Category analysis
            if 'category' in df.columns:
                category_stats = df.groupby('category').agg({
                    'price': ['count', 'mean', 'sum'],
                    'quantity': 'sum'
                }).round(2).to_dict()
            else:
                category_stats = {}
            
            processed_data = {
                'total_products': total_products,
                'total_value': total_value,
                'avg_price': avg_price,
                'low_stock_products': low_stock,
                'out_of_stock_products': out_of_stock,
                'total_stock_value': total_stock_value,
                'category_statistics': category_stats,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            self.processed_data['products'] = processed_data
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing product data: {str(e)}")
            return {}
    
    def process_order_data(self, data: List[Dict]) -> Dict[str, Any]:
        """
        Process order data and generate insights
        """
        try:
            df = pd.DataFrame(data)
            
            # Basic statistics
            total_orders = len(df)
            total_revenue = df['total_amount'].sum() if 'total_amount' in df.columns else 0
            avg_order_value = df['total_amount'].mean() if 'total_amount' in df.columns else 0
            
            # Date analysis
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['month'] = df['created_at'].dt.month
                df['year'] = df['created_at'].dt.year
                df['day_of_week'] = df['created_at'].dt.day_name()
                
                monthly_revenue = df.groupby(['year', 'month'])['total_amount'].sum().to_dict()
                daily_revenue = df.groupby('day_of_week')['total_amount'].sum().to_dict()
                recent_orders = len(df[df['created_at'] >= datetime.now() - timedelta(days=7)])
            else:
                monthly_revenue = {}
                daily_revenue = {}
                recent_orders = 0
            
            # Status analysis
            if 'status' in df.columns:
                status_counts = df['status'].value_counts().to_dict()
            else:
                status_counts = {}
            
            processed_data = {
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'avg_order_value': avg_order_value,
                'monthly_revenue': monthly_revenue,
                'daily_revenue': daily_revenue,
                'recent_orders': recent_orders,
                'status_distribution': status_counts,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            self.processed_data['orders'] = processed_data
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing order data: {str(e)}")
            return {}
    
    def generate_report(self, report_type: str = 'comprehensive') -> Dict[str, Any]:
        """
        Generate comprehensive report from processed data
        """
        try:
            report = {
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'summary': {},
                'details': self.processed_data
            }
            
            # Generate summary statistics
            if 'customers' in self.processed_data:
                report['summary']['customers'] = {
                    'total': self.processed_data['customers'].get('total_customers', 0),
                    'active': self.processed_data['customers'].get('active_customers', 0),
                    'recent': self.processed_data['customers'].get('recent_customers', 0)
                }
            
            if 'products' in self.processed_data:
                report['summary']['products'] = {
                    'total': self.processed_data['products'].get('total_products', 0),
                    'total_value': self.processed_data['products'].get('total_value', 0),
                    'low_stock': self.processed_data['products'].get('low_stock_products', 0)
                }
            
            if 'orders' in self.processed_data:
                report['summary']['orders'] = {
                    'total': self.processed_data['orders'].get('total_orders', 0),
                    'total_revenue': self.processed_data['orders'].get('total_revenue', 0),
                    'avg_order_value': self.processed_data['orders'].get('avg_order_value', 0)
                }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {}
    
    def export_to_csv(self, data: List[Dict], filename: str) -> bool:
        """
        Export data to CSV file
        """
        try:
            if not data:
                logger.warning("No data to export")
                return False
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            logger.info(f"Data exported to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return False
    
    def export_to_json(self, data: Dict, filename: str) -> bool:
        """
        Export data to JSON file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Data exported to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}")
            return False
    
    def validate_data(self, data: List[Dict], required_fields: List[str]) -> List[str]:
        """
        Validate data for required fields
        """
        errors = []
        
        for i, record in enumerate(data):
            for field in required_fields:
                if field not in record or record[field] is None:
                    errors.append(f"Record {i+1}: Missing required field '{field}'")
        
        return errors

class DataAnalyzer:
    """Advanced data analysis class"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_customer_trends(self, customer_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze customer trends and patterns
        """
        try:
            df = pd.DataFrame(customer_data)
            
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                
                # Growth trends
                df['date'] = df['created_at'].dt.date
                daily_signups = df.groupby('date').size()
                
                # Calculate growth rate
                growth_rate = daily_signups.pct_change().mean()
                
                # Predict future growth
                trend = daily_signups.rolling(window=7).mean()
                
                analysis = {
                    'total_customers': len(df),
                    'growth_rate': growth_rate,
                    'daily_signups_avg': daily_signups.mean(),
                    'trend_data': trend.to_dict(),
                    'peak_signup_day': daily_signups.idxmax().strftime('%Y-%m-%d'),
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
                self.analysis_results['customer_trends'] = analysis
                return analysis
                
        except Exception as e:
            logger.error(f"Error analyzing customer trends: {str(e)}")
            return {}
    
    def analyze_sales_patterns(self, order_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze sales patterns and seasonality
        """
        try:
            df = pd.DataFrame(order_data)
            
            if 'created_at' in df.columns and 'total_amount' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                
                # Daily sales patterns
                daily_sales = df.groupby(df['created_at'].dt.date)['total_amount'].sum()
                
                # Weekly patterns
                df['day_of_week'] = df['created_at'].dt.day_name()
                weekly_pattern = df.groupby('day_of_week')['total_amount'].sum()
                
                # Monthly patterns
                df['month'] = df['created_at'].dt.month
                monthly_pattern = df.groupby('month')['total_amount'].sum()
                
                # Peak sales analysis
                peak_sales_day = daily_sales.idxmax()
                peak_sales_amount = daily_sales.max()
                
                analysis = {
                    'total_revenue': df['total_amount'].sum(),
                    'avg_daily_sales': daily_sales.mean(),
                    'peak_sales_day': peak_sales_day.strftime('%Y-%m-%d'),
                    'peak_sales_amount': peak_sales_amount,
                    'weekly_pattern': weekly_pattern.to_dict(),
                    'monthly_pattern': monthly_pattern.to_dict(),
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
                self.analysis_results['sales_patterns'] = analysis
                return analysis
                
        except Exception as e:
            logger.error(f"Error analyzing sales patterns: {str(e)}")
            return {}

def main():
    """Main function for data processing"""
    processor = DataProcessor()
    analyzer = DataAnalyzer()
    
    # Example usage
    logger.info("Starting data processing...")
    
    # Process sample data (you would load real data here)
    sample_customers = [
        {'name': 'John Doe', 'email': 'john@example.com', 'source': 'website'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'source': 'referral'}
    ]
    
    # Process data
    customer_stats = processor.process_customer_data(sample_customers)
    customer_trends = analyzer.analyze_customer_trends(sample_customers)
    
    # Generate report
    report = processor.generate_report('comprehensive')
    
    # Export results
    processor.export_to_json(report, 'crm_report.json')
    
    logger.info("Data processing completed!")

if __name__ == "__main__":
    main()
