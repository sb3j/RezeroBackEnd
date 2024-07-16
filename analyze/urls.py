from django.urls import path
from django.conf.urls.static import static
from .views import UploadImageView, DalleResultAPIView, RequestDesignView
from django.conf import settings

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('dalle_result/', DalleResultAPIView.as_view(), name='dalle-result'),
    path('request/', RequestDesignView.as_view(), name='request-design'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)