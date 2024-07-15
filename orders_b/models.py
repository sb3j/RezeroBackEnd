from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company')
    business_registration_number = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, default='', blank=True, null=True)
    detail_address = models.CharField(max_length=255, default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Fix(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    sleeve_length = models.CharField(max_length=15)
    neckline = models.CharField(max_length=20)
    pocket = models.CharField(max_length=10, blank=True, null=True)
    etc = models.CharField(max_length=10)
    material = models.CharField(max_length=20)  # 추가된 필드
    color = models.CharField(max_length=20)  # 추가된 필드
    created_at = models.DateTimeField(auto_now_add=True)