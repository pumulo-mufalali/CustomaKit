"""
API endpoints for customer management
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import json
from .models import Customer
from .utils import get_customer_statistics, search_customers, validate_customer_data, export_customer_data

@csrf_exempt
@require_http_methods(["GET"])
def customer_list_api(request):
    """
    Get paginated list of customers
    """
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '')
        
        if search:
            customers = search_customers(search)
        else:
            customers = Customer.objects.all().order_by('-created_at')
        
        paginator = Paginator(customers, per_page)
        customers_page = paginator.get_page(page)
        
        data = {
            'customers': list(customers_page.object_list.values()),
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_count': paginator.count
        }
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def customer_detail_api(request, customer_id):
    """
    Get specific customer details
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'source': customer.source,
            'created_at': customer.created_at.isoformat(),
            'is_active': customer.is_active
        }
        
        return JsonResponse(data, safe=False)
    
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_customer_api(request):
    """
    Create a new customer
    """
    try:
        data = json.loads(request.body)
        
        # Validate data
        errors = validate_customer_data(data)
        if errors:
            return JsonResponse({'errors': errors}, status=400)
        
        # Create customer
        customer = Customer.objects.create(
            name=data['name'],
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            source=data.get('source', 'website')
        )
        
        response_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'source': customer.source,
            'created_at': customer.created_at.isoformat()
        }
        
        return JsonResponse(response_data, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_customer_api(request, customer_id):
    """
    Update customer information
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        data = json.loads(request.body)
        
        # Update fields
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'source' in data:
            customer.source = data['source']
        if 'is_active' in data:
            customer.is_active = data['is_active']
        
        customer.save()
        
        response_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'source': customer.source,
            'is_active': customer.is_active,
            'updated_at': customer.created_at.isoformat()
        }
        
        return JsonResponse(response_data)
    
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_customer_api(request, customer_id):
    """
    Delete a customer
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        
        return JsonResponse({'message': 'Customer deleted successfully'})
    
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def customer_statistics_api(request):
    """
    Get customer statistics
    """
    try:
        stats = get_customer_statistics()
        return JsonResponse(stats)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def export_customers_api(request):
    """
    Export customers data
    """
    try:
        format_type = request.GET.get('format', 'csv')
        data = export_customer_data(format_type)
        
        if data:
            response = JsonResponse({'data': data})
            response['Content-Type'] = 'text/csv'
            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            return response
        else:
            return JsonResponse({'error': 'Export failed'}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
