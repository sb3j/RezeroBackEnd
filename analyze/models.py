from django.db import models
from django.conf import settings

class OrderInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/before/')
    before_image_url = models.URLField(max_length=2000, null=True, blank=True)  # URL 필드 추가
    uploaded_at = models.DateTimeField(auto_now_add=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    neck_line = models.CharField(max_length=50, null=True, blank=True)
    sleeve_length = models.CharField(max_length=50, null=True, blank=True)
    pattern = models.CharField(max_length=50, null=True, blank=True)
    pocket = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    button = models.CharField(max_length=50, null=True, blank=True)
    addt_design = models.CharField(max_length=100, null=True, blank=True)
    dalle_image_url = models.URLField(max_length=2000, null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)
