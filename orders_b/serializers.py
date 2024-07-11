from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    original_category = serializers.ChoiceField(choices=Order.ORIGINAL_CATEGORY_CHOICES)
    desired_category = serializers.ChoiceField(choices=Order.DESIRED_CATEGORY_CHOICES)

    class Meta:
        model = Order
        fields = [
            'id', 
            'order_number',
            'customer_nickname',
            'customer_order_number',
            'original_category',
            'desired_category',
            'order_date',
            'due_date',
            'status'
        ]
