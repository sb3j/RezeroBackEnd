# analyze/urls.py
from django.urls import path
from .views import upload_image, dalle_result

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('dalle_result/', dalle_result, name='dalle_result'),
]
