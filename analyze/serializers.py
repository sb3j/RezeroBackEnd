from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['user', 'image', 'uploaded_at', 'material', 'category', 'color', 'neck_line', 
                  'sleeve_length', 'pattern', 'pocket', 'zip', 'button', 'b_shape', 'b_color', 
                  'addt_design', 'dalle_image_url', 'prompt']
