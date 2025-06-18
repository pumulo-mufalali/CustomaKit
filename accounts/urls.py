from django.urls import path
from .views import *


urlpatterns = [
  path('', dashboard, name='dashboard'),
  path('customers/', customers, name='customers'),
  path('customer/<int:pk>/', customer, name='customer_detail'),
  path('products/', products, name='product'),
  path('status/', status, name='statuses'),
  path('create_order/', create_order, name='create_order'),
]