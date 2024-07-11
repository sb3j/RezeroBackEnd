# analyze/urls.py
from django.urls import path
from .views import upload_image, dalle_result, create_order  # create_order 추가

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('dalle_result/', dalle_result, name='dalle_result'),
    path('create_order/', create_order, name='create_order'),  # create_order 경로 추가
]
