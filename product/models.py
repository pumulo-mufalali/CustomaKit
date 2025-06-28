from django.db import models
from customer.models import Customer

class Tag(models.Model):
  name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.name

class Product(models.Model):
  name = models.CharField(max_length=70, null=True)
  price = models.FloatField(null=True)
  description = models.CharField(max_length=100, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField(Tag)

  def __str__(self):
    return self.name


class Order(models.Model):
  STATUS = (
    ('delivered', 'delivered'),
    ('Intransit', 'Intransit'),
    ('pending', 'pending'),
  )

  customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
  status = models.CharField(max_length=100, null=True, choices=STATUS)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.status
