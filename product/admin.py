from django.contrib import admin
from .models import Product, Order, Tag

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
