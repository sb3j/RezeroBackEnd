from rest_framework import serializers
from .models import OrderUser
from orders_b.models import Company

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUser
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'category', 'material', 'color']  # material, color 필드를 read_only로 설정

    def validate_neckline(self, value):
        category = self.instance.category if self.instance else self.initial_data.get('category')
        if category == 'shirt' and value not in ['round', 'v_neck', 'square', 'collar']:
            raise serializers.ValidationError("Invalid neckline choice for shirt.")
        if category == 'sweater' and value not in ['round', 'v_neck', 'square', 'collar', 'turtle']:
            raise serializers.ValidationError("Invalid neckline choice for sweater.")
        return value

    def validate(self, data):
        category = self.instance.category if self.instance else data.get('category')
        if category == 'shirt' and ('button' in data or 'zipper' in data):
            raise serializers.ValidationError("Shirts/T-shirts do not have buttons or zippers.")
        return data

    def validate_company(self, value):
        try:
            company = Company.objects.get(id=value)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company ID")
        return value