from django.urls import path
from . import views


urlpatterns = [
  path('products/', views.products, name='product_list'),
  path('status/', views.status, name='statuses'),

  path('orders/', views.totalOrders, name='total_orders'),

  path('create_product/', views.createProduct, name='create_product'),

  path('create_order/<int:pk>/', views.createOrder, name='create_order'),
  path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
  path('delete_order/<int:pk>/', views.deleteOrder, name='delete'),

  path('delete_product/<int:pk>/', views.deleteProduct, name='delete'),
]