from django.db import models

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    ORIGINAL_CATEGORY_CHOICES = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        ('category3', 'Category 3'),
    ]

    DESIRED_CATEGORY_CHOICES = [
        ('result1', 'Result 1'),
        ('result2', 'Result 2'),
        ('result3', 'Result 3'),
    ]

    order_number = models.AutoField(primary_key=True)
    customer_nickname = models.CharField(max_length=100)
    customer_order_number = models.CharField(max_length=100)
    original_category = models.CharField(max_length=100, choices=ORIGINAL_CATEGORY_CHOICES)
    desired_category = models.CharField(max_length=100, choices=DESIRED_CATEGORY_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f'Order {self.order_number}'