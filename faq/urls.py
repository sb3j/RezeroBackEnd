# faq/urls.py
from django.urls import path
from .views import FAQListCreateAPIView, FAQRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', FAQListCreateAPIView.as_view(), name='faq-list'),
    path('<int:pk>/', FAQRetrieveUpdateDestroyAPIView.as_view(), name='faq-detail'),
]
