from django.urls import path
from . import views


urlpatterns = [
  path('login/', views.loginPage, name='login'),
  path('register/', views.registerPage, name='register'),

  path('', views.dashboard, name='dashboard'),
  path('customer/<int:pk>/', views.customer, name='customer_detail'),
  path('products/', views.products, name='product'),
  path('status/', views.status, name='statuses'),

  path('customers/', views.customers, name='customers'),
  path('orders/', views.totalOrders, name='total_orders'),

  path('create_order/<int:pk>/', views.createOrder, name='create_order'),
  path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
  path('delete_order/<int:pk>/', views.deleteOrder, name='delete'),

  path('create_customer/', views.createCustomer, name='create_customer'),
  # path('update_customer/<int:pk>/', updateCustomer, name='update_customer'),
  # path('delete_customer/<int:pk>/', deleteCustomer, name='delete_customer'),
]