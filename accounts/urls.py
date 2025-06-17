from django.urls import path
from .views import dashboard, products, customer, status


urlpatterns = [
  path('', dashboard),
  path('customer/', customer),
  path('products/', products),
  path('status/', status),
]