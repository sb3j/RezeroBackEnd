from rest_framework import serializers
from .models import Order, Fix
from analyze.models import OrderInfo
from users.models import CustomUser
from django.db import models

class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = [
            'image', 'before_image_url', 'uploaded_at', 'material', 'category', 'color', 
            'neck_line', 'sleeve_length', 'pattern', 'pocket', 'zip', 'button', 
            'addt_design', 'dalle_image_url', 'prompt'
        ]

class OrderSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    detail_address = serializers.CharField(source='user.detail_address', read_only=True)
    ordered_company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    order_info = OrderInfoSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'company_name', 'username', 'nickname', 'phone', 'address', 
            'detail_address', 'ordered_company_name', 'order_info', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'username', 'nickname', 'phone', 'address', 'detail_address', 
            'ordered_company_name', 'order_info', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        company_name = validated_data.pop('company_name')

        try:
            business_user = CustomUser.objects.get(company_name=company_name, user_type='business')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Business user not found")

        try:
            order_info = OrderInfo.objects.filter(user=user).latest('uploaded_at')
        except OrderInfo.DoesNotExist:
            raise serializers.ValidationError("No order info found for the user")

        # 주문 수 카운트 업데이트
        user.orders_count = models.F('orders_count') + 1
        user.save()

        # 주문 요청 수 카운트 업데이트
        business_user.order_requests_count = models.F('order_requests_count') + 1
        business_user.save()

        order = Order.objects.create(
            user=user,
            order_info=order_info,
            business_user=business_user,
            user_nickname=user.nickname,
            material=order_info.material,
            category=order_info.category,
            color=order_info.color,
            **validated_data
        )
        return order

class OrderRequestSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    material = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_nickname', 'material', 'category', 'color', 'created_at']




from rest_framework import serializers
from .models import Fix

class FixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fix
        fields = ['id', 'user_nickname', 'material', 'category', 'color', 'created_at', 'fixed_at', 'deadline', 'is_completed']
        read_only_fields = ['created_at', 'fixed_at', 'deadline', 'is_completed']

class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['company_name']
        


# class OrderInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderInfo
#         fields = ['uploaded_at', 'material', 'category']



class UserOrderSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    status = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'company_name', 'status', 'category']

    def get_status(self, obj):
        try:
            if Fix.objects.filter(order=obj).exists():
                fix = Fix.objects.get(order=obj)
                if fix.is_completed:
                    return '완료'
                return '수락'
        except Fix.DoesNotExist:
            pass

        try:
            Order.objects.get(id=obj.id)
            return '대기'
        except Order.DoesNotExist:
            return '거절'

    def get_category(self, obj):
        return obj.order_info.category if obj.order_info else None

class UserOrderDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    status = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    before_image_url = serializers.CharField(source='order_info.before_image_url', read_only=True)
    dalle_image_url = serializers.CharField(source='order_info.dalle_image_url', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'company_name', 'category', 'before_image_url', 'dalle_image_url', 'status']

    def get_status(self, obj):
        try:
            if Fix.objects.filter(order=obj).exists():
                fix = Fix.objects.get(order=obj)
                if fix.is_completed:
                    return '완료'
                return '수락'
        except Fix.DoesNotExist:
            pass

        try:
            Order.objects.get(id=obj.id)
            return '대기'
        except Order.DoesNotExist:
            return '거절'

    def get_category(self, obj):
        return obj.order_info.category if obj.order_info else None