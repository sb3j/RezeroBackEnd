# analyze/models.py
from django.db import models

class OrderInfo(models.Model):
    image = models.ImageField(upload_to='images/before/')
    result_image = models.ImageField(upload_to='images/after/', blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    neck_line = models.CharField(max_length=100, blank=True, null=True)
    sleeve_length = models.CharField(max_length=100, blank=True, null=True)
    pattern = models.CharField(max_length=100, blank=True, null=True)
    pocket = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    button = models.CharField(max_length=100, blank=True, null=True)
    addt_design = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"OrderInfo({self.id})"

