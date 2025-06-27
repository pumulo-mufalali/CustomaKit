from django.urls import path
from . import views

urlpatterns = [
  path('products/', views.products, name='product'),
  path('status/', views.status, name='statuses'),

  
  path('orders/', views.totalOrders, name='total_orders'),

  path('create_order/<int:pk>/', views.createOrder, name='create_order'),
  path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
  path('delete_order/<int:pk>/', views.deleteOrder, name='delete'),
]