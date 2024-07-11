# analyze/urls.py
from django.urls import path
from .views import upload_image, result_image

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('result/', result_image, name='result_image'),
]
