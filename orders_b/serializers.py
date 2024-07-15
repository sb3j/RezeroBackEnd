from rest_framework import serializers
from orders_u.models import OrderUser
from orders_b.models import Fix

class OrderUserListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname')
    category_display = serializers.CharField(source='get_category_display')

    class Meta:
        model = OrderUser
        fields = ['id', 'nickname', 'category_display', 'created_at']


from rest_framework import serializers
from .models import Company  

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']




from rest_framework import serializers
from orders_u.models import OrderUser
from users.models import CustomUser 
from orders_b.models import Company  

class OrderUserDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname')
    category_display = serializers.CharField(source='get_category_display')
    user = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = OrderUser
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "phone": user.phone, 
            "address": user.address,  
            "detail_address": user.detail_address  
        }

    def get_company(self, obj):
        company = obj.company
        return {
            "id": company.id,
            "name": company.name,
            "registration_number": company.business_registration_number,
            "phone": company.phone,
            "address": company.address,
            "detail_address": company.detail_address
        }

class FixSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname')
    category_display = serializers.CharField(source='get_category_display')
    user = serializers.SerializerMethodField()

    class Meta:
        model = Fix
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "phone": user.phone,
            "address": user.address,
            "detail_address": user.detail_address
        }