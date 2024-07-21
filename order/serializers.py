from rest_framework import serializers
from .models import Order, Fix
from analyze.models import OrderInfo
from users.models import CustomUser
from django.db import models

#주문하고나서 들어가는것들
class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = [
            'image', 'before_image_url', 'uploaded_at', 'material', 'category', 'color', 
            'neck_line', 'sleeve_length', 'pattern', 'pocket', 'zip', 'button', 
            'addt_design', 'dalle_image_url', 'prompt'
        ]

#주문하고나서 들어가는것들
class OrderSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    detail_address = serializers.CharField(source='user.detail_address', read_only=True)
    ordered_company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    order_info = OrderInfoSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'company_name', 'username', 'nickname', 'phone', 'address', 
            'detail_address', 'ordered_company_name', 'order_info', 
            'created_at', 'updated_at', 'status_display'
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

    def get_status_display(self, obj):
        return obj.get_status_display()

#주문요청할때
class OrderRequestSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    material = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_nickname', 'material', 'category', 'color', 'created_at', 'status_display']

    def get_status_display(self, obj):
        return obj.get_status_display()




from rest_framework import serializers
from .models import Fix

#기업이 수락한 주문들어가는 테이블
class FixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fix
        fields = ['id', 'user_nickname', 'material', 'category', 'color', 'created_at', 'fixed_at', 'deadline', 'is_completed']
        read_only_fields = ['created_at', 'fixed_at', 'deadline', 'is_completed']

#기업이름조회
class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['company_name']
        

#사용자 주문내역
class UserOrderSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'company_name', 'status_display', 'category']

    def get_category(self, obj):
        return obj.order_info.category if obj.order_info else None


#사용자 주문 상세
class UserOrderDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='business_user.company_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category = serializers.CharField(source='order_info.category', read_only=True)
    before_image_url = serializers.CharField(source='order_info.before_image_url', read_only=True)
    dalle_image_url = serializers.CharField(source='order_info.dalle_image_url', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    detail_address = serializers.CharField(source='user.detail_address', read_only=True)
    sleeve_length = serializers.CharField(source='order_info.sleeve_length', read_only=True)
    pattern = serializers.CharField(source='order_info.pattern', read_only=True)
    pocket = serializers.CharField(source='order_info.pocket', read_only=True)
    zip = serializers.CharField(source='order_info.zip', read_only=True)
    button = serializers.CharField(source='order_info.button', read_only=True)
    addt_design = serializers.CharField(source='order_info.addt_design', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'created_at', 'company_name', 'category', 'before_image_url', 'dalle_image_url',
            'status_display', 'address', 'detail_address', 'sleeve_length', 'pattern', 'pocket', 
            'zip', 'button', 'addt_design'
        ]

# class UserOrderDetailSerializer(serializers.ModelSerializer):
#     company_name = serializers.CharField(source='business_user.company_name', read_only=True)
#     status_display = serializers.CharField(source='get_status_display', read_only=True)
#     category = serializers.SerializerMethodField()
#     before_image_url = serializers.CharField(source='order_info.before_image_url', read_only=True)
#     dalle_image_url = serializers.CharField(source='order_info.dalle_image_url', read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'created_at', 'company_name', 'category', 'before_image_url', 'dalle_image_url', 'status_display']

#     def get_category(self, obj):
#         return obj.order_info.category if obj.order_info else None
