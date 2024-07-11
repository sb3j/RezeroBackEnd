from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('admin', 'Admin')
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class ReceiveOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('accepted', '수락'),
        ('rejected', '거절'),
    ]

    CLOTHING_CATEGORY_CHOICES = [
        ('shirt', '셔츠'),
        ('tshirt', '티셔츠'),
        ('sweater', '스웨터'),
    ]

    order_number = models.CharField(max_length=100)
    customer_order_number = models.CharField(max_length=6)  # 6자리 알파벳+숫자 조합
    clothing_category = models.CharField(max_length=100, choices=CLOTHING_CATEGORY_CHOICES)  # 의류 카테고리 추가
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    customer_email = models.EmailField()
    customer_address = models.CharField(max_length=255)
    order_title = models.CharField(max_length=255)
    order_content = models.TextField()
    preference_collar = models.BooleanField(default=False)
    preference_pocket = models.BooleanField(default=False)
    image_before = models.ImageField(upload_to='orders/before/')
    image_after = models.ImageField(upload_to='orders/after/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)
    business_user = models.ForeignKey(CustomUser, related_name='received_orders', on_delete=models.CASCADE, limit_choices_to={'user_type': 'business'})

    def __str__(self):
        return self.order_title
