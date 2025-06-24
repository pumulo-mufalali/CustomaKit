from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  phone = models.CharField(max_length=200, null=True)
  profile_pic = models.ImageField(null=True, blank=True)
  email = models.CharField(max_length=200, null=True, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name[:50]
  

class Tag(models.Model):
  name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.name

class Product(models.Model):
  CATEGORY = (
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
  )

  name = models.CharField(max_length=70, null=True)
  price = models.FloatField(null=True)
  category = models.CharField(max_length=50, null=True, choices=CATEGORY)
  description = models.CharField(max_length=100, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField(Tag)

  def __str__(self):
    return self.name


class Order(models.Model):
  STATUS = (
    ('delivered', 'delivered'),
    ('Out for delivery', 'Out for delivery'),
    ('pending', 'pending'),
  )

  customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
  status = models.CharField(max_length=100, null=True, choices=STATUS)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.status