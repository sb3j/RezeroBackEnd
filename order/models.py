from django.db import models
from django.conf import settings
from analyze.models import OrderInfo 
from users.models import CustomUser
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_orders')
    user_nickname = models.CharField(max_length=150)
    material = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class Fix(models.Model):
    user_nickname = models.CharField(max_length=150)
    material = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    fixed_at = models.DateTimeField(auto_now_add=True)
    business_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='fixed_orders')