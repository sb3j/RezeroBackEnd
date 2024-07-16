# from rest_framework import serializers
# from .models import UploadedImage

# class UploadedImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadedImage
#         fields = ['user', 'image', 'uploaded_at', 'material', 'category', 'color', 'neck_line', 
#                   'sleeve_length', 'pattern', 'pocket', 'zip', 'button', 'b_shape', 'b_color', 
#                   'addt_design', 'dalle_image_url', 'prompt']

from rest_framework import serializers
from .models import OrderInfo

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['user', 'image', 'uploaded_at', 'material', 'category', 'color', 'neck_line', 
                  'sleeve_length', 'pattern', 'pocket', 'zip', 'button', 'b_shape', 'b_color', 
                  'addt_design', 'dalle_image_url', 'prompt']

class DesignRequestSerializer(serializers.Serializer):
    neck_line = serializers.CharField(required=False)
    sleeve_length = serializers.CharField(required=False)
    pattern = serializers.CharField(required=False)
    pocket = serializers.CharField(required=False)
    zip = serializers.CharField(required=False)
    button = serializers.CharField(required=False)
    b_shape = serializers.CharField(required=False)
    b_color = serializers.CharField(required=False)
    addt_design = serializers.CharField(required=False)
