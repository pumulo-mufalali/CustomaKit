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