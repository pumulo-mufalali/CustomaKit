from django.urls import path
from . import views

urlpatterns = [
  path('customer/<int:pk>/', views.customer, name='customer_detail'),
  path('customers/', views.customers, name='customers'),
  path('create_customer/', views.createCustomer, name='create_customer'),
  path('update_customer/<int:pk>/', views.updateCustomer, name='update_customer'),

]