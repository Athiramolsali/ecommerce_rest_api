from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    created_by_id=models.ForeignKey(User, on_delete=models.CASCADE,)
    # Add any other relevant fields for customers

class Product(models.Model):
    name = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')
    active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(default=timezone.now)
