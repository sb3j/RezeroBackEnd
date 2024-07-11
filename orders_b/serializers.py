from rest_framework import serializers
from .models import ReceiveOrder

class ReceiveOrderRequestListSerializer(serializers.ModelSerializer):
    customer_nickname = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = ReceiveOrder
        fields = [
            'id', 
            'customer_nickname',
            'customer_order_number',
            'clothing_category',
            'order_date',
            'order_title',
        ]


class ReceiveOrderListSerializer(serializers.ModelSerializer):
    customer_nickname = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = ReceiveOrder
        fields = [
            'id',  
            'customer_nickname',
            'customer_order_number',
            'clothing_category',
            'order_date',
            'order_title',
        ]

class ReceiveOrderSerializer(serializers.ModelSerializer):
    customer_nickname = serializers.CharField(source='customer.username', read_only=True)
    business_user_nickname = serializers.CharField(source='business_user.username', read_only=True)

    class Meta:
        model = ReceiveOrder
        fields = [
            'id',
            'order_number',
            'order_date',
            'customer_nickname',
            'customer_email',
            'customer_address',
            'order_title',
            'order_content',
            'preference_collar',
            'preference_pocket',
            'image_before',
            'image_after',
            'status',
            'business_user_nickname',
        ]
