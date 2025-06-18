from django.urls import path
from .views import *


urlpatterns = [
  path('', dashboard, name='dashboard'),
  path('customer/<int:pk>/', customer, name='customer_detail'),
  path('products/', products, name='product'),
  path('status/', status, name='statuses'),

  path('customers/', customers, name='customers'),
  path('orders/', total_orders, name='total_orders'),

  path('create_order/', create_order, name='create_order'),
  path('create_customer/', create_customer, name='create_customer'),
]