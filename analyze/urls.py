from django.urls import path
from .views import UploadImageView, DalleResultAPIView, RequestDesignView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('dalle_result/', DalleResultAPIView.as_view(), name='dalle-result'),
    path('request/', RequestDesignView.as_view(), name='request-design'),
]
