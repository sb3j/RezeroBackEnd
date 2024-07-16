from django.urls import path
from .views import UploadImageView, DalleResultAPIView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('dalle_result/', DalleResultAPIView.as_view(), name='dalle-result'),
]
