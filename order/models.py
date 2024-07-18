from django.db import models
from django.conf import settings
from analyze.models import OrderInfo 
from users.models import CustomUser
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta

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
    created_at = models.DateTimeField(auto_now_add=True)
    fixed_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()  # 새로운 필드 추가
    is_completed = models.BooleanField(default=False)  # 완료 상태 필드 추가
    business_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='fixed_orders')

    def save(self, *args, **kwargs):
        if not self.id: 
            self.deadline = self.created_at + timedelta(days=7)
        if self.deadline.date() == timezone.now().date():
            self.is_completed = True
        super(Fix, self).save(*args, **kwargs)

# class Fix(models.Model):
#     user_nickname = models.CharField(max_length=150)
#     material = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     color = models.CharField(max_length=100)
#     created_at = models.DateTimeField()
#     fixed_at = models.DateTimeField(auto_now_add=True)
#     business_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='fixed_orders')