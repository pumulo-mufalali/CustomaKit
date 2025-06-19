from django.urls import path
from .views import *


urlpatterns = [
  path('', dashboard, name='dashboard'),
  path('customer/<int:pk>/', customer, name='customer_detail'),
  path('products/', products, name='product'),
  path('status/', status, name='statuses'),

  path('customers/', customers, name='customers'),
  path('orders/', totalOrders, name='total_orders'),

  path('create_order/', createOrder, name='create_order'),
  path('update_order/<int:pk>/', updateOrder, name='update_order'),
  path('create_customer/', createCustomer, name='create_customer'),
]